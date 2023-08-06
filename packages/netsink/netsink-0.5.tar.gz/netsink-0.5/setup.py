#!/usr/bin/env python

# Netsink - Network Sinkhole for Isolated Malware Analysis
# Copyright (C) 2013-2014 Steve Henderson
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

def load_version():
    "Returns the current project version"
    from netsink import version
    return version.__version__

setup(
    name="netsink",
    version=load_version(),
    packages=['netsink', 'netsink.modules'],
    zip_safe=False,
    author="Steve Henderson",
    author_email="steve.henderson@hendotech.com.au",
    url="https://github.com/shendo/netsink",
    description="Network Sinkhole for Isolated Malware Analysis",
    long_description=open('README.rst').read(),
    entry_points={"console_scripts": ['netsink = netsink.start:main'],
                  "netsink.modules": ['dns = netsink.modules.dns:DNSHandler',
                                      'http = netsink.modules.http:HTTPHandler',
                                      'irc = netsink.modules.ircserver:IRCHandler',
                                      'dispatcher = netsink.modules.multi:Dispatcher',
                                      'smtp = netsink.modules.smtp:SMTPHandler',
                                      'ssl = netsink.modules.sslwrap:SSLHandler',
                                      'ftp = netsink.modules.ftp:FTPHandler']
          },
    include_package_data=True,
    license="GPL",
    install_requires = open('requirements.txt').readlines(),
    tests_require = ['pytest>=2.5'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Security'
    ],
)
