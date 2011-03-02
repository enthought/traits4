import glob
from os.path import splitext

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


ext_modules = [
    Extension(splitext(path)[0], [path]) for path in glob.glob('*.pyx')
]


setup(
    cmdclass    = {'build_ext': build_ext},
    ext_modules = ext_modules
)

#### EOF ######################################################################
