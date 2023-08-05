#!/usr/bin/python
# -*- coding: utf-8 -*-

# messages.py file is part of slpkg.

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
from colors import colors
from __metadata__ import __all__

def pkg_not_found(bol, pkg, message, eol):
    '''
    Print message when package not found
    '''
    print("{0}No such package {1}: {2}{3}".format(bol, pkg, message, eol))

def pkg_found(pkg, version):
    '''
    Print message when package found
    '''
    print("| Package {0}-{1} is already installed".format(pkg, version))

def pkg_installed(pkg):
    '''
    Print message when package installed
    '''
    print("| Package {0} installed".format(pkg))

def ext_err_args():
    '''
    Extended error arguments view
    '''
    print("usage: {0} [-h] [-v] [-a script [sources ...]]".format(__all__))
    print("             [-l all, sbo, slack, noarch] [-c sbo, slack [<upgrade> ...]]")
    print("             [-s sbo, slack [<package> ...]] [-t] [-n] [-i  [...]]")
    print("             [-u  [...]] [-o  [...]] [-r  [...]] [-f  [...]] [-d  [...]]")

def err1_args(invalid, choices):
    '''
    Print error message arguments
    '''
    print("{0}: error: invalid choice: '{1}' choose from {2}".format(
            __all__, invalid, choices))

def err2_args(choices):
    '''
    Print error message arguments
    '''
    print("{0}: error: must enter at least two arguments: choose {1}".format(
            __all__, choices))

def s_user(user):
    '''
    Check for root user
    '''
    if user != "root":
        print("\nError: must have root privileges\n")
        sys.exit()

def build_FAILED(sbo_url, prgnam):
    template(78)
    print("| Build package {0} [ {1}FAILED{2} ]".format(prgnam, colors.RED, colors.ENDC))
    template(78)
    print("| See log file in {0}/var/log/slpkg/sbo/build_logs{1} directory or read README file:".format(
          colors.CYAN, colors.ENDC))
    print("| {0}{1}".format(sbo_url, "README"))
    template(78)
    print # new line at end

def template(max):
    '''
    Print view template
    '''
    print("+" + "=" * max)

def view_sbo(pkg, sbo_url, sbo_dwn, source_dwn, sbo_req):
    print # new line at start
    template(78)
    print("| {0}Package {1}{2}{3} --> {4}".format(colors.GREEN,
            colors.CYAN, pkg, colors.GREEN, colors.ENDC + sbo_url))
    template(78)
    print("| {0}SlackBuild : {1}{2}".format(colors.GREEN, colors.ENDC, sbo_dwn))
    print("| {0}Sources : {1}{2}".format(colors.GREEN, colors.ENDC, source_dwn))
    print("| {0}Requirements : {1}{2}".format(colors.YELLOW, colors.ENDC,
                                               ", ".join(sbo_req)))
    template(78)
    print(" {0}R{1}EADME               View the README file".format(colors.RED, colors.ENDC))
    print(" {0}S{1}lackBuild           View the SlackBuild file".format(colors.RED, colors.ENDC))
    print(" In{0}f{1}o                 View the Info file".format(colors.RED, colors.ENDC))
    print(" {0}D{1}ownload             Download this package".format(colors.RED, colors.ENDC))
    print(" {0}B{1}uild                Download and build".format(colors.RED, colors.ENDC))
    print(" {0}I{1}nstall              Download/Build/Install".format(colors.RED, colors.ENDC))
    print(" {0}Q{1}uit                 Quit\n".format(colors.RED, colors.ENDC))

