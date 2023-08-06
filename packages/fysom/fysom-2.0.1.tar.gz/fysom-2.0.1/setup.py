#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'fysom',
          version = '2.0.1',
          description = '''pYthOn Finite State Machine''',
          long_description = '''''',
          author = "Mansour Behabadi, Jake Gordon, Maximilien Riehl, Stefano",
          author_email = "mansour@oxplot.com, jake@codeincomplete.com, maximilien.riehl@gmail.com, ",
          license = 'MIT',
          url = 'https://github.com/mriehl/fysom',
          scripts = [],
          packages = ['fysom'],
          py_modules = [],
          classifiers = ['Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python', 'Natural Language :: English', 'Operating System :: OS Independent', 'Topic :: Scientific/Engineering'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          
          
          zip_safe=True
    )
