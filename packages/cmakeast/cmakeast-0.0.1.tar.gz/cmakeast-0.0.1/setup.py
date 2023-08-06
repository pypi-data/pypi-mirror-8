# /setup.py
#
# Installation and setup script for cmakeast
#
# See LICENCE.md for Copyright information

from setuptools import setup, find_packages

setup(name='cmakeast',
      version='0.0.1',
      description='CMake AST',
      long_description='Reduce a CMake file to an abstract syntax tree',
      author='Sam Spilsbury',
      author_email='smspillaz@gmail.com',
      classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Developers',
           'Topic :: Software Development :: Build Tools',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
      ],
      license='MIT',
      keywords='development ast cmake',
      packages=find_packages(exclude=['tests']),
      extras_require={
          'test': ['coverage']
      },
      entry_points={
          'console_scripts': [
              'cmake-print-ast=cmakeast.printer:main'
          ]
      },
      test_suite="nose.collector")
