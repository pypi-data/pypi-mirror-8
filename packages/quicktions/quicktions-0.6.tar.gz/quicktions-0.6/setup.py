
import sys
import re
from distutils.core import setup, Extension

ext_modules = [
    Extension("quicktions", ["src/quicktions.pyx"]),
]

try:
    sys.argv.remove("--with-cython")
except ValueError:
    cythonize = None
else:
    try:
        from Cython.Build import cythonize
        import Cython.Compiler.Options as cython_options
        cython_options.annotate = True
    except ImportError:
        cythonize = None
    else:
        ext_modules = cythonize(ext_modules)

if cythonize is None:
    for ext_module in ext_modules:
        ext_module.sources[:] = [m.replace('.pyx', '.c') for m in ext_module.sources]


with open('src/quicktions.pyx') as f:
    version = re.search("__version__\s*=\s*'([^']+)'", f.read(2048)).group(1)

with open('README.rst') as f:
    long_description = ''.join(f.readlines()[3:]).strip()

with open('CHANGES.rst') as f:
    long_description += '\n\n' + f.read()


setup(
    name="quicktions",
    version=version,
    description="Fast fractions data type for rational numbers. "
                "Cythonized version of 'fractions.Fraction'.",
    long_description=long_description,
    author="Stefan Behnel",
    author_email="stefan_ml@behnel.de",
    bugtrack_url="https://github.com/scoder/quicktions/issues",

    ext_modules=ext_modules,
    package_dir={'': 'src'},

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: Python Software Foundation License",
    ],
)
