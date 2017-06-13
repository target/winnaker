#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='winnaker',
      description='An audit tool that tests the whole system functionality of Spinnaker',
      author='Target Corporation',
      version='0.2.0',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'selenium==3.4.3',
          'pyvirtualdisplay==0.2',
          'tqdm==4.8.4',
      ],
      entry_points={
          "console_scripts": [
              "winnaker = winnaker.main:main"
          ]
      }
      )
