#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='bigbluebutton_api_python_medad',
      version='0.0.14',
      description='Python library that provides access to the API of BigBlueButton',
      author='Tarek Kalaji, Hicham Dachir',
      author_email='dachirhicham@gmail.com',
      url='https://github.com/HichamDz38/bigbluebutton-api-python',
      packages=find_packages(),
      install_requires=[
          'jxmlease'
      ],
)
