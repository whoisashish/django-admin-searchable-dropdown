import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-admin-searchable-dropdown',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    description='A simple Django app to render list filters in dropdown format with search option',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/whoisashish/django-admin-searchable-dropdown',
    author='Ashish Yadav',
    author_email='anujashish1602@gmail.com',
    install_requires=[
        'django>=2.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
