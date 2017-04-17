#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='winnaker',
      description='An audit tool that tests the whole system functionality of Spinnaker',
      author='Target Corporation',
      packages=find_packages(),
      install_requires=[
          'selenium',
          'pyvirtualdisplay',
          'tqdm',
      ],
      entry_points={
          "console_scripts": [
              "winnaker = winnaker.main:main"
          ]
      }
      )
