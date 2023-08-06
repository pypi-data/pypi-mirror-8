from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksDownloader',
    version='0.1.2',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Core functionalities for geospatial data download.',
    install_requires=[
        'geobricksmodis'
    ],
    url='http://pypi.python.org/pypi/GeobricksDownloader/'
)
