from distutils.core import setup, Extension

pycorels = Extension('pycorels',
                    sources = ['pycorels.c'],
                    libraries = ['corels', 'gmpxx', 'gmp'],
                    library_dirs = ['~/code/bbcache/src'])

setup (name = 'pycorels',
       version = '0.1',
       description = 'Python binding of CORELS algorithm',
       ext_modules = [pycorels])
