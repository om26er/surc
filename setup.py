import os

from setuptools import setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

VERSION = '0.1.0'

setup(
    name='surc',
    version=VERSION,
    packages=['database'],
    url='https://github.com/om26er/surc',
    license='GNU GPL Version 3',
    author='Omer Akram',
    author_email='om26er@gmail.com',
    description='Snap Upstream Release Checker',
    download_url='https://github.com/om26er/surc/tarball/{}'.format(VERSION),
    keywords=['linux', 'ubuntu'],
    install_requires=['SQLAlchemy', 'requests', 'PyYAML'],
)
