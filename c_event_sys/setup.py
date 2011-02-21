from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('messages', ['messages.pyx']),
               Extension('signals', ['signals.pyx']),
               Extension('dispatchers', ['dispatchers.pyx'])]

setup(cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules)
