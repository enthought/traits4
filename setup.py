from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('c_event_sys.messages', ['c_event_sys/messages.pyx']),
               Extension('c_event_sys.signals', ['c_event_sys/signals.pyx']),
               Extension('c_event_sys.dispatchers', ['c_event_sys/dispatchers.pyx']),
               #Extension('c_core._trait_types', ['c_core/_trait_types.pyx']),
               #Extension('c_core._has_traits', ['c_core/_has_traits.pyx']),
               ]

setup(cmdclass = {'build_ext': build_ext},
      ext_modules = ext_modules)
