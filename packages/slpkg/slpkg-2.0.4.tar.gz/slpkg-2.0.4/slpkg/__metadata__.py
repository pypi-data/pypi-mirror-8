#!/usr/bin/python
# -*- coding: utf-8 -*-

# __metadata__.py

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os

__all__ = "slpkg"
__author__ = "dslackw"
__version_info__ = (2, 0, 4)
__version__ = "{0}.{1}.{2}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "d.zlatanidis@gmail.com"

''' file spacer '''
sp = "-"

''' current path '''
path = os.getcwd() + "/"

''' build path '''
build_path = path + "slpkg_Build/"

''' library path '''
lib_path = "/var/lib/slpkg/"

''' log path '''
log_path = "/var/log/slpkg/"

''' temponary path '''
tmp = "/tmp/"
slpkg_tmp = tmp + "slpkg/"

''' packages log files path '''
pkg_path = "/var/log/packages/"

''' blacklist conf path '''
bls_path = "/etc/slpkg/"

''' computer architecture '''
arch = os.uname()[4]
