from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
	Extension("aramada", ["main.py"]),
]

setup(
	name='My Program',
	cmdclass={'build_ext': build_ext},
	ext_modules=ext_modules,

)
