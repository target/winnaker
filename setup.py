#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='winnaker',
      description='An audit tool that tests the whole system functionality of Spinnaker',
      author='Target Corporation',
      version='1.0.3',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'selenium==3.4.3',
          'pyvirtualdisplay==0.2',
          'tqdm==4.8.4',
          'retrying==1.3.3',
          'python-dotenv==0.6.4'
      ],
      entry_points={
          "console_scripts": [
              "winnaker = winnaker.main:main"
          ]
      }
      )
