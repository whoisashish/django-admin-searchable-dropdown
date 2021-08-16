# encoding: utf-8

import os
from setuptools import find_packages, setup

VERSION = '1.0.5'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

description = 'Provides Searchable Dropdown Filters for Django Admin'
long_description = description
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

setup(
    name='django-admin-searchable-dropdown',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description=description,
    long_description=long_description,
    url='https://github.com/whoisashish/django-admin-searchable-dropdown',
    download_url='https://github.com/whoisashish/django-admin-searchable-dropdown/archive/%s.zip' % VERSION,
    author='Ashish Yadav',
    author_email="yadavobito@gmail.com",
    keywords=['searchable', 'search', 'django', 'admin', 'filter', 'dropdown'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
