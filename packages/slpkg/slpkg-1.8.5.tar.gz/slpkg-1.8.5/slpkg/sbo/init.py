#!/usr/bin/python
# -*- coding: utf-8 -*-

# init.py file is part of slpkg.

# Copyright 2014 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Utility for easy management packages in Slackware

# https://github.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
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
import sys

from slpkg.url_read import url_read
from slpkg.__metadata__ import log_path, lib_path

from slpkg.slack.slack_version import slack_ver

from file_size import server_file_size, local_file_size

def initialization():
    '''
    Slpkg initialization, creating directories and SLACKBUILDS.TXT in 
    /var/lib/slpkg/sbo_repo/ and ChangeLog.txt in /var/log/slpkg/ from
    slackbuilds.org
    '''
    sbo_log = log_path + "sbo/"
    sbo_lib = lib_path + "sbo_repo/"
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    if not os.path.exists(lib_path):
        os.mkdir(lib_path)
    if not os.path.exists(sbo_log):
        os.mkdir(sbo_log)
    if not os.path.exists(sbo_lib):
        os.mkdir(sbo_lib)
    sbo_url = ("http://slackbuilds.org/slackbuilds/{0}/".format(slack_ver()))
    '''
    Read SLACKBUILDS.TXT from slackbuilds.org and write in /var/lib/slpkg/sbo_repo/
    directory if not exist
    '''
    if not os.path.isfile(sbo_lib + "SLACKBUILDS.TXT"):
        print("\nslpkg ...initialization")
        sys.stdout.write("SLACKBUILDS.TXT read ...")
        sys.stdout.flush()
        SLACKBUILDS_TXT = url_read((
            "http://slackbuilds.org/slackbuilds/{0}/SLACKBUILDS.TXT".format(slack_ver())))
        sys.stdout.write("Done\n")
        sbo = open("{0}SLACKBUILDS.TXT".format(sbo_lib), "w")
        sbo.write(SLACKBUILDS_TXT)
        sbo.close()
        print("File SLACKBUILDS.TXT created in {0}".format(sbo_lib))
    '''
    Read ChangeLog.txt from slackbuilds.org and write in /var/log/slpkg/sbo/
    directory if not exist
    '''
    if not os.path.isfile(sbo_log + "ChangeLog.txt"):
        print("\nslpkg initialization")
        sys.stdout.write("ChangeLog.txt read ...")
        sys.stdout.flush()
        ChangeLog_txt = url_read((
            "http://slackbuilds.org/slackbuilds/{0}/ChangeLog.txt".format(slack_ver())))
        sys.stdout.write("Done\n")
        log = open("{0}ChangeLog.txt".format(sbo_log), "w")
        log.write(ChangeLog_txt)
        log.close()
        print("File ChangeLog.txt created in {0}".format(sbo_log))
    '''
    We take the size of ChangeLog.txt from the server and locally
    '''
    server = int(''.join(server_file_size(sbo_url + "ChangeLog.txt")))
    local = int(local_file_size(sbo_log + "ChangeLog.txt"))
    '''
    If the two files differ in size delete and replaced with new
    '''
    if server != local:
        os.remove("{0}{1}".format(sbo_lib, "SLACKBUILDS.TXT"))
        os.remove("{0}{1}".format(sbo_log, "ChangeLog.txt"))
        print("\nNEWS in ChangeLog.txt")
        print("slpkg ...initialization")
        sys.stdout.write("Files re-created ...")
        sys.stdout.flush()
        SLACKBUILDS_TXT = url_read((
            "http://slackbuilds.org/slackbuilds/{0}/SLACKBUILDS.TXT".format(slack_ver())))
        ChangeLog_txt = url_read((
            "http://slackbuilds.org/slackbuilds/{0}/ChangeLog.txt".format(slack_ver())))
        sbo = open("{0}SLACKBUILDS.TXT".format(sbo_lib), "w")
        sbo.write(SLACKBUILDS_TXT)
        sbo.close()
        log = open("{0}ChangeLog.txt".format(sbo_log), "w")
        log.write(ChangeLog_txt)
        log.close()
        sys.stdout.write("Done\n")
