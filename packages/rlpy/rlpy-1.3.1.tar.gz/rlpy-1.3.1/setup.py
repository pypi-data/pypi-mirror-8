"""
Installation script for RLPy
"""

from setuptools import setup, Extension, find_packages
from Cython.Distutils import build_ext
import numpy
import os
import sys

version = '1.3.1'

if sys.platform == 'darwin':
    # by default use clang++ as this most likely to have c++11 support
    # on OSX
    if "CC" not in os.environ or os.environ["CC"] == "":
        os.environ["CC"] = "clang++"
        extra_args = ["-std=c++0x", "-stdlib=libc++"]
else:
    extra_args = []

setup(name="rlpy",
      version=version,
      maintainer="Christoph Dann",
      maintainer_email="cdann@cdann.de",
      license="BSD 3-clause",
      description="Value-Function-Based Reinforcement-Learning Library for"
                  + " Education and Research",
      url="http://acl.mit.edu/rlpy/",
      classifiers=['Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Programming Language :: C++',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Operating System :: MacOS',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                  ],
      long_description=open('README.rst').read(),
      packages=find_packages(exclude=['tests', 'tests.*']),
      include_package_data=True,
#      package_data={'rlpy': [
#          'Domains/GridWorldMaps/*.txt',
#          'Domains/IntruderMonitoringMaps/*.txt',
#          'Domains/PinballConfigs/*.cfg',
#          'Domains/PacmanPackage/layouts/*.lay',
#          'Domains/SystemAdministratorMaps/*.txt',
#          "Representations/c_kernels.h",
#      ]
#      },
      install_requires=[
          'numpy >= 1.7',
          'scipy',
          'matplotlib >= 1.2',
          'networkx',
          'scikit-learn',
          'joblib',
          'hyperopt',
          'pymongo'
      ],
      extras_require={'cython_extensions': ['cython']},
      cmdclass={'build_ext': build_ext},
      ext_modules=[
          Extension("rlpy.Representations.hashing",
                    ["rlpy/Representations/hashing.pyx"],
                    include_dirs=[numpy.get_include(), "rlpy/Representations"]),
          Extension("rlpy.Domains.HIVTreatment_dynamics",
                    ["rlpy/Domains/HIVTreatment_dynamics.pyx"],
                    include_dirs=[numpy.get_include(), "rlpy/Representations"]),
          Extension("rlpy.Representations.kernels",
                    ["rlpy/Representations/kernels.pyx",
                     "rlpy/Representations/c_kernels.cc",
                     "rlpy/Representations/c_kernels.pxd"],
                    language="c++",
                    include_dirs=[numpy.get_include(), "rlpy.Representations"]),
          Extension("rlpy.Tools._transformations",
                    ["rlpy/Tools/transformations.c"],
                    include_dirs=[numpy.get_include()])],
      test_suite='tests'
      )
