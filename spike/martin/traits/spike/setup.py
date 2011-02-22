
# copy these lines to a file named: setup.py
# To build and install the elemlist module you need the following
# setup.py file that uses the distutils:
from distutils.core import setup, Extension

setup (name = "elemlist",
       version = "1.0",
       maintainer = "Alex Martelli",
       maintainer_email = "aleax@aleax.it",
       description = "Sample Python module",

       ext_modules = [Extension('simpletype',sources=['simpletype.c'])]
       ##ext_modules = [Extension('noddy',sources=['noddy.c'])]
)
