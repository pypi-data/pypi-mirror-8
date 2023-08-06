# -*- coding: utf-8 -*-
import sys
from setuptools import setup, Extension

SOURCES = ['src/py_minizip.c', 'src/zip.c', 'src/ioapi.c']
LIBRARIES = ['z']

if 'win32' in sys.platform:
    SOURCES.append('src/iowin32.c')
    LIBRARIES = ['zlib']

setup(
    name = 'pyminizip',
    version = '0.2.0',
    description = 'A minizip wrapper - To create a password encrypted zip file in python.',
    author='Shin Aoyama',
    author_email = "smihica@gmail.com",
    url = "https://github.com/smihica/pyminizip",
    download_url = "",
    keywords = ["zip", "file", "compress", "password", "encryption"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: zlib/libpng License",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    ext_modules=[
        Extension(name="pyminizip",
                  sources=SOURCES,
                  include_dirs=['src'],
                  libraries=LIBRARIES,
                  )
        ],
    long_description = """\
To create a password encrypted zip file in python.
And the zip file is able to extract in WINDOWS.

This is a simple Minizip wrapper of python.
(http://www.winimage.com/zLibDll/minizip.html)

This software uses zlib.
License: zlib/libpng License.

install zlib

    linux:
    $ sudo apt-get install zlib
    mac:
    $ sudo port install zlib

install pyminizip

    $ pip install pyminizip

----------------------------------------------------------------------------

Provides two functions.
==============================

pyminizip.compress("/srcfile/path.txt", "/distfile/path.zip", "password", int(compress_level))

  Args:
  1. src file path (string)
  2. dst file path (string)
  3. password (string) or None (to create no-password zip)
  4. compress_level(int) between 1 to 9, 1 (more fast) <---> 9 (more compress) or 0 (default)

  Return value:
  - always returns None

pyminizip.compress_multiple([u'pyminizip.so', 'file2.txt'], "file.zip", "1233", 4)
  Args:
  1. src file LIST path (list)
  2. dst file path (string)
  3. password (string) or None (to create no-password zip)
  4. compress_level(int) between 1 to 9, 1 (more fast)  <---> 9 (more compress)

  Return value:
  - always returns None


==============================
""",
    )
