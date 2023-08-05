#!/usr/bin/python
# -*- coding: utf-8 -*-

# views.py file is part of slpkg.

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
import pydoc

from slpkg.colors import *
from slpkg.init import initialization
from slpkg.downloader import download
from slpkg.__metadata__ import tmp, build_path, pkg_path, sp
from slpkg.messages import (pkg_not_found, pkg_found, view_sbo, 
                            template, build_FAILED)

from slpkg.pkg.build import build_package
from slpkg.pkg.find import find_package
from slpkg.pkg.manager import pkg_upgrade

from read import *
from greps import *
from search import sbo_search_pkg
from download import sbo_slackbuild_dwn

def sbo_network(name):
    '''
    View SlackBuild package, read or install them 
    from slackbuilds.org
    '''
    done = "{0}Done{1}\n".format(GREY, ENDC)
    reading_lists = "{0}Reading package lists ...{1}".format(GREY, ENDC)
    sys.stdout.write(reading_lists)
    sys.stdout.flush()
    init = initialization()
    sbo_url = sbo_search_pkg(name)
    if sbo_url:
        sbo_desc = sbo_description_pkg(name)[len(name) + 2:-1]
        sbo_req = sbo_requires_pkg(name)
        sbo_dwn = sbo_slackbuild_dwn(sbo_url)
        source_dwn = sbo_source_dwn(name).split()
        sys.stdout.write(done)
        view_sbo(name, sbo_url, sbo_desc, sbo_dwn.split("/")[-1], \
                 ", ".join([src.split("/")[-1] for src in source_dwn]), \
                 sbo_req)
        # Check if package supported by arch
        # before proceed to install
        FAULT = str()
        UNST = ["UNSUPPORTED", "UNTESTED"]
        if "".join(source_dwn) in UNST:
            FAULT = "".join(source_dwn)
        while True:
            try:
                read = raw_input(" {0}Choose an option: {1}".format(GREY, ENDC))
            except KeyboardInterrupt:
                print # new line at exit
                break
            if read == "D" or read == "d":
                path = ""
                download(path, sbo_dwn)
                for src in source_dwn:
                    download(path, src)
                break
            elif read == "R" or read == "r":
                readme = "README"
                pydoc.pager(read_readme(sbo_url, readme))
            elif read == "F" or read == "f":
                _info = ".info"
                pydoc.pager(read_info_slackbuild(sbo_url, name, _info))
            elif read == "S" or read == "s":
                _SlackBuild = ".SlackBuild"
                pydoc.pager(read_info_slackbuild(sbo_url, name, _SlackBuild))
            elif read == "B" or read == "b":
                if FAULT:
                    print("\n{0}The package {1} {2}\n".format(RED, FAULT, ENDC))
                    sys.exit()
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                sources = []
                os.chdir(build_path)
                script = sbo_dwn.split("/")[-1] # get file from script link
                download(build_path, sbo_dwn)
                for src in source_dwn:
                    download(build_path, src)
                    sources.append(src.split("/")[-1]) # get file from source link
                build_package(script, sources, build_path)
                break
            elif read == "I" or read == "i":
                if FAULT:
                    print("\n{0}The package {1} {2}\n".format(RED, FAULT, ENDC))
                    sys.exit()
                if not os.path.exists(build_path):
                    os.mkdir(build_path)
                sbo_version = sbo_version_pkg(name)
                prgnam = ("{0}-{1}".format(name, sbo_version))
                if find_package(prgnam + sp, pkg_path) == []:
                    sources = []
                    os.chdir(build_path)
                    download(build_path, sbo_dwn)
                    script = sbo_dwn.split("/")[-1] # get file from script link
                    for src in source_dwn:
                            download(build_path, src)
                            sources.append(src.split("/")[-1]) # get file from source link
                    build_package(script, sources, build_path)
                    # Searches the package name and version in /tmp to install.
                    # If find two or more packages e.g. to build tag 
                    # 2 or 3 will fit most.
                    binary_list = []
                    for search in find_package(prgnam, tmp):
                        if "_SBo" in search:
                            binary_list.append(search)
                    try:
                        binary = (tmp + max(binary_list)).split()
                    except ValueError:
                        build_FAILED(sbo_url, prgnam)
                        sys.exit()
                    print("{0}[ Installing ] --> {1} {2}".format(GREEN, ENDC, name))
                    pkg_upgrade(binary)
                    break
                else:
                    template(78)
                    pkg_found(name, sbo_version)
                    template(78)
                    break
            else:
                break
    else:
        sys.stdout.write (done)
        message = "From slackbuilds.org"
        pkg_not_found("\n", name, message, "\n")
