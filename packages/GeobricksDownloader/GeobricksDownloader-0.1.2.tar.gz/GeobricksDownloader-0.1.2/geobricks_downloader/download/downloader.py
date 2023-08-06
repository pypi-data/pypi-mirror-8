import uuid
from types import DictType
from importlib import import_module
from geobricks_downloader.utils import log
from geobricks_downloader.utils.filesystem import create_filesystem
from geobricks_downloader.download.downloads_thread_manager import DownloadsThreadManager


class Downloader():

    # Mandatory parameters.
    source = None
    file_paths_and_sizes = None

    # This can be a string with the target folder or a hierarchical tree
    # e.g. {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1', 'year': '2014', 'day': '033'}
    filesystem_structure = None

    # Optional parameters.
    username = None
    password = None
    threaded = False

    # Derived parameters.
    source_type = 'FTP'
    config = None
    target_dir = None
    download_manager = None

    def __init__(self, source, file_system_structure, file_paths_and_sizes,
                 threaded=False, block_size=16384, username=None, password=None):

        """
        @type source:                   str
        @param source:                  e.g. 'modis', either lower or upper case.

        @type file_system_structure:    str | dict
        @param file_system_structure:   This parameter can be either a String, representing the target directory for the
                                        downloads (e.g. '/home/user/Desktop'), or a Dict, describing the file system
                                        structure (e.g. {'target': '/home/kalimaha/Desktop/MODIS', 'product': 'MOD13Q1',
                                        'year': '2014', 'day': '033'})

        @type file_paths_and_sizes:     collection
        @param file_paths_and_sizes:    Collection of objects containing the following fields: 'file_name', 'size',
                                        'file_path', 'label'.

        @type threaded:                 bool
        @param threaded:                Run the downloader in multiple or single thread mode.

        @type block_size:               float
        @param block_size:              The remote file is downloaded in chunk, each one of 'block_size' size.

        @type username:                 str
        @param username:                Optional parameter.

        @type password:                 str
        @param password:                Optional parameter.

        """

        # Store parameters.
        self.source = source.lower()
        self.file_paths_and_sizes = file_paths_and_sizes
        self.file_system_structure = file_system_structure
        self.username = username
        self.password = password
        self.threaded = threaded
        self.block_size = block_size

        # Load configuration
        module_name = 'geobricks_' + self.source + '.config.' + self.source + '_config'
        mod = import_module(module_name)
        self.config = getattr(mod, 'config')

        # Derive other parameters.
        self.log = log.logger(self.__class__.__name__)
        self.source_type = self.config['source']['type']
        self.target_dir = file_system_structure
        self.uuid = str(uuid.uuid4())
        if type(file_system_structure) is DictType:
            self.target_dir = file_system_structure['target']
            self.target_dir = create_filesystem(self.target_dir, self.file_system_structure, self.config)

    def download(self):
        self.download_manager = DownloadsThreadManager(self.uuid, self.target_dir, self.file_paths_and_sizes, self.threaded)
        self.download_manager.start()
        return self.download_manager.downloaded_files

    def progress(self, filename):
        return self.download_manager.progress(filename)