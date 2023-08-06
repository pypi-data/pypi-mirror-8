__author__ = 'lobocv'

from distutils.core import setup
from pyperform import __version__

setup(
    name='pyperform',
    packages=['pyperform'],  # this must be the same as the name above
    version=__version__,
    description='A convenient way to performance test functions and compare results. TEST TEST TEST',
    author='Calvin Lobo',
    author_email='calvinvlobo@gmail.com',
    url='https://github.com/lobocv/pyperform',
    download_url='https://github.com/lobocv/pyperform/tarball/1.4',
    keywords=['testing', 'performance', 'comparison', 'convenience', 'logging'],
    classifiers=[],
)