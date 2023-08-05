#!/usr/bin/env python
import numpy as np
import os
from numpy.distutils.core import setup
from numpy.distutils.extension import Extension
from hooks import get_cmdclass, get_version

# force sdist to copy files
delattr(os, 'link')

VERSION = '4.1'

name = 'qubic'
long_description = open('README.rst').read()
keywords = 'scientific computing'
platforms = 'MacOS X,Linux,Solaris,Unix,Windows'
extra_f90_compile_args = ['-cpp -fopenmp -fpack-derived']

ext_modules = [Extension('qubic._flib',
                         sources=['src/polarization.f90.src'],
                         extra_f90_compile_args=extra_f90_compile_args,
                         include_dirs=['.', np.get_include()],
                         libraries=['gomp'])]

setup(name=name,
      version=get_version(name, VERSION),
      description='Simulation and map-making tools for the QUBIC experiment.',
      long_description=long_description,
      url='',
      author='Pierre Chanial',
      author_email='pierre.chanial@apc.univ-paris7.fr',
      install_requires=['progressbar',
                        'pyoperators>=0.12.12',
                        'pysimulators>=1.0',
                        'healpy>=0.6.1',
                        'pyYAML'],
      packages=['qubic', 'qubic/io'],
      package_data={'qubic': ['calfiles/*fits', 'data/*', 'scripts/*py']},
      platforms=platforms.split(','),
      keywords=keywords.split(','),
      cmdclass=get_cmdclass(),
      ext_modules=ext_modules,
      license='CeCILL-B',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 2 :: Only',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy'])
