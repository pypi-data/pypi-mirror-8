#!/usr/bin/python
# -*- coding: utf-8 -*-

# dependency.py file is part of slpkg.

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

import sys

from slpkg.colors import colors
from slpkg.__metadata__ import pkg_path, sp
from slpkg.messages import pkg_not_found, template

from slpkg.pkg.find import find_package

from init import initialization
from search import sbo_search_pkg
from greps import sbo_requires_pkg

dep_results = []

def sbo_dependencies_pkg(name):
    '''
    Build all dependencies of a package
    '''
    try:
        dependencies = []
        sbo_url = sbo_search_pkg(name)
        if sbo_url:
            requires = sbo_requires_pkg(sbo_url, name)
            for req in requires:
                if "%README%" not in req:
                    dependencies.append(req)
            if dependencies:
                dep_results.append(dependencies)
                for dep in dependencies:
                    sys.stdout.write("{0}.{1}".format(
                                     colors.GREY, colors.ENDC))
                    sys.stdout.flush()
                    sbo_dependencies_pkg(dep)
            return dep_results
    except KeyboardInterrupt:
        print # new line at exit
        sys.exit()

def pkg_tracking(name):
    '''
    View tree of dependencies and also
    highlight packages with color green  
    if allready installed and color red
    if not installed.
    '''
    sys.stdout.write("{0}Reading package lists ...{1}".format(
                     colors.GREY, colors.ENDC))
    sys.stdout.flush()
    initialization()
    dependencies_list = sbo_dependencies_pkg(name)
    GREEN, RED = colors.GREEN, colors.RED
    YELLOW, CYAN, ENDC = colors.YELLOW, colors.CYAN, colors.ENDC
    if dependencies_list is not None:
        sys.stdout.write("{0}Done{1}\n".format(colors.GREY, colors.ENDC))
        print # new line at start
        requires, dependencies = [], []
        '''
        Create one list for all packages
        '''
        for pkg in dependencies_list:
            requires += pkg
        requires.reverse()
        '''
        Remove double dependencies
        '''
        for duplicate in requires:
            if duplicate not in dependencies:
                dependencies.append(duplicate)
        if dependencies == []:
            dependencies = ["No dependencies"]
        pkg_len = len(name) + 24
        template(pkg_len)
        print("| Package {0}{1}{2} dependencies :".format(CYAN, name, ENDC))
        template(pkg_len)
        print("\\")
        print(" +---{0}[ Tree of dependencies ]{1}".format(YELLOW, ENDC))
        index = 0
        for pkg in dependencies:
            index += 1
            if find_package(pkg + sp, pkg_path):
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, GREEN, pkg, ENDC))
            else:
                print(" |")
                print(" {0}{1}: {2}{3}{4}".format("+--", index, RED, pkg, ENDC))
        print # new line at end
    else:
        sys.stdout.write("{0}Done{1}\n".format(colors.GREY, colors.ENDC))
        message = "From slackbuilds.org"
        pkg_not_found("\n", name, message, "\n")
