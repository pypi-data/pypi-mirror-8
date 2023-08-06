#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from webdav.client import __version__ as version

setup(
    name     = 'webdavclient',
    version  = version,
    packages = find_packages(),
    requires = ['python (>= 2.7.6)'],
    install_requires=['pycurl', 'lxml', 'argcomplete'],
    scripts = ['wdc'],
    description  = 'Webdav API, resource API and webdav tool for WebDAV servers (Yandex.Disk, Dropbox, Google Disk, Box, 4shared)',
    long_description = open('README.rst').read(),
    author = 'Designerror',
    author_email = 'designerror@yandex.ru',
    url          = 'https://github.com/designerror/webdavclient',
    download_url = 'https://github.com/designerror/webdavclient/tarball/master',
    license      = 'MIT License',
    keywords     = 'webdav, client, python, module, library, packet, Yandex.Disk, Dropbox, Google Disk, Box, 4shared',
    classifiers  = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
