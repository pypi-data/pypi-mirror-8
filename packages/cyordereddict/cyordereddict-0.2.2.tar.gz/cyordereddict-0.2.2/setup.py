import os.path
import sys
from distutils.core import setup
from distutils.extension import Extension

# adapted from cytoolz: https://github.com/pytoolz/cytoolz/blob/master/setup.py

VERSION = '0.2.2'

if sys.version_info[0] == 2:
    base_dir = 'python2'
elif sys.version_info[0] == 3:
    base_dir = 'python3'

filename = os.path.join(base_dir, 'cyordereddict', '_version.py')
with open(filename, 'w') as f:
    f.write('__version__ = %r' % VERSION)

try:
    from Cython.Build import cythonize
    has_cython = True
except ImportError:
    has_cython = False

is_dev = 'dev' in VERSION
use_cython = is_dev or '--cython' in sys.argv or '--with-cython' in sys.argv
if '--no-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--no-cython')
if '--without-cython' in sys.argv:
    use_cython = False
    sys.argv.remove('--without-cython')
if '--cython' in sys.argv:
    sys.argv.remove('--cython')
if '--with-cython' in sys.argv:
    sys.argv.remove('--with-cython')

if use_cython and not has_cython:
    if is_dev:
        raise RuntimeError('Cython required to build dev version of cyordereddict.')
    print('WARNING: Cython not installed.  Building without Cython.')
    use_cython = False

ext = '.pyx' if use_cython else '.c'
source = os.path.join(base_dir, "cyordereddict", "_cyordereddict")
ext_modules = [Extension("cyordereddict._cyordereddict", [source + ext])]
if use_cython:
    ext_modules = cythonize(ext_modules)

if __name__ == '__main__':
    setup(
        name='cyordereddict',
        description="Cython implementation of Python's collections.OrderedDict",
        long_description=(open('README.rst').read()
                          if os.path.exists('README.rst')
                          else ''),
        version=VERSION,
        license='MIT',
        url='https://github.com/shoyer/cyordereddict',
        author='Stephan Hoyer',
        author_email='shoyer@gmail.com',
        packages=['cyordereddict', 'cyordereddict.benchmark'],
        package_dir={'': base_dir},
        ext_modules=ext_modules,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Cython',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
        ],
    )
