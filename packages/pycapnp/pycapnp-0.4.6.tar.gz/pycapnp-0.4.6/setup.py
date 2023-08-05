#!/usr/bin/env python
try:
    from Cython.Build import cythonize
    import Cython
except ImportError:
    raise RuntimeError('No cython installed. Please run `pip install cython`')

if Cython.__version__ < '0.19.1':
    raise RuntimeError('Old cython installed (%s). Please run `pip install -U cython`' % Cython.__version__)

import pkg_resources
setuptools_version = pkg_resources.get_distribution("setuptools").version
if setuptools_version < '0.8':
    raise RuntimeError('Old setuptools installed (%s). Please run `pip install -U setuptools`. Running `pip install pycapnp` will not work alone, since setuptools needs to be upgraded before installing anything else.' % setuptools_version)

from distutils.core import setup
import os

MAJOR = 0
MINOR = 4
MICRO = 6
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'

from .lib.capnp import _CAPNP_VERSION_MAJOR as LIBCAPNP_VERSION_MAJOR
from .lib.capnp import _CAPNP_VERSION_MINOR as LIBCAPNP_VERSION_MINOR
from .lib.capnp import _CAPNP_VERSION_MICRO as LIBCAPNP_VERSION_MICRO
from .lib.capnp import _CAPNP_VERSION as LIBCAPNP_VERSION
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'capnp', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (VERSION, VERSION))
    finally:
        a.close()

write_version_py()

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''

from distutils.command.clean import clean as _clean
class clean(_clean):
    def run(self):
        _clean.run(self)
        for x in [ 'capnp/lib/capnp.cpp', 'capnp/lib/capnp.h', 'capnp/version.py' ]:
            print('removing %s' % x)
            try:
                os.remove(x)
            except OSError:
                pass

setup(
    name="pycapnp",
    packages=["capnp"],
    version=VERSION,
    package_data={'capnp': ['*.pxd', '*.h', '*.capnp', 'helpers/*.pxd', 'helpers/*.h', 'includes/*.pxd', 'lib/*.pxd', 'lib/*.py', 'lib/*.pyx']},
    ext_modules=cythonize('capnp/lib/*.pyx'),
    cmdclass = {
        'clean': clean
    },
    install_requires=[
        'cython >= 0.21',
        'setuptools >= 0.8'],
    # PyPi info
    description="A cython wrapping of the C++ Cap'n Proto library",
    long_description=long_description,
    license='BSD',
    author="Jason Paryani",
    author_email="pypi-contact@jparyani.com",
    url = 'https://github.com/jparyani/pycapnp',
    download_url = 'https://github.com/jparyani/pycapnp/archive/v%s.zip' % VERSION,
    keywords = ['capnp', 'capnproto', "Cap'n Proto"],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: C++',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Communications'],
)
