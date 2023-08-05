#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from distutils.core import Command

setup(
    name='django-calaccess-raw-data',
    version='0.0.8',
    packages=[
        'calaccess_raw',
        'calaccess_raw.admin',
        'calaccess_raw.management',
        'calaccess_raw.management.commands',
        'calaccess_raw.models',
    ],
    include_package_data=True,
    license='MIT',
    description='A Django app to download, extract and load campaign \
finance and lobbying activity data from the California \
Secretary of State\'s CAL-ACCESS database',
    url='https://github.com/california-civic-data-coalition',
    author='California Civic Data Coalition',
    author_email='ben.welsh@latimes.com',
    install_requires=(
        'django>=1.6',
        'csvkit==0.6.1',
        'python-dateutil==2.1',
        'MySQL-python==1.2.5',
        'argparse==1.2.1',
        'requests==2.2.1',
        'progressbar>=2.2',
        'hurry.filesize==0.9',
    ),
)
