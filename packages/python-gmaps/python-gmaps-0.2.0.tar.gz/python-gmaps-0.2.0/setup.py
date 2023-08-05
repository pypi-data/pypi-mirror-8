# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), 'src', 'gmaps', '__init__.py')
version_line = list(filter(lambda l: l.startswith('VERSION'), open(init)))[0]
VERSION = get_version(eval(version_line.split('=')[-1]))

INSTALL_REQUIRES = reqs('requirements.txt')

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
PACKAGES = find_packages('src')
PACKAGE_DIR = {'': 'src'}

setup(
    name='python-gmaps',
    version=VERSION,
    author='Michał Jaworski',
    author_email='swistakm@gmail.com',
    description='Google Maps API client',
    long_description=README,

    packages=PACKAGES,
    package_dir=PACKAGE_DIR,

    url='https://github.com/swistakm/python-gmaps',
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
