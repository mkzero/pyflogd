#!/usr/bin/env python2

from setuptools import setup

setup(name='pyflogd',
      version='0.1.1',
      description='File system access monitoring daemon',
      author='Izzy Kulbe',
      author_email='pyflogd@unikorn.me',
      license='MIT',
      packages=['pyflogd'],
      entry_points = {
        "console_scripts": [
          "pyflogd = pyflogd.pyflogd:main",
        ],
      },
      install_requires=[
        'pyinotify',
        'docopt',
        'schema',
        'python-daemon',
        'lockfile',
      ],
    )
