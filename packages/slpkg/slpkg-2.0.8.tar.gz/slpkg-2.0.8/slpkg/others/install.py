#!/usr/bin/python
# -*- coding: utf-8 -*-

# install.py file is part of slpkg.

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

from slpkg.sizes import units
from slpkg.repositories import Repo
from slpkg.init import Initialization
from slpkg.blacklist import BlackList
from slpkg.splitting import split_package
from slpkg.messages import (
    pkg_not_found,
    template
)
from slpkg.__metadata__ import (
    pkg_path,
    lib_path,
    log_path,
    slpkg_tmp_packages,
    default_answer,
    color
)

from slpkg.pkg.find import find_package
from slpkg.pkg.manager import PackageManager

from slpkg.slack.remove import delete
from slpkg.slack.slack_version import slack_ver

from greps import repo_data
from download import packages_dwn
from dependency import dependencies_pkg


class OthersInstall(object):

    def __init__(self, package, repo, version):
        self.package = package
        self.repo = repo
        self.version = version
        self.tmp_path = slpkg_tmp_packages
        self.repo_init()
        repos = Repo()
        print("\nPackages with name matching [ {0}{1}{2} ]\n".format(
              color['CYAN'], self.package, color['ENDC']))
        sys.stdout.write("{0}Reading package lists ...{1}".format(
            color['GREY'], color['ENDC']))
        sys.stdout.flush()
        self.step = 700
        repos = Repo()
        if self.repo == "rlw":
            lib = lib_path + "rlw_repo/PACKAGES.TXT"
            self.mirror = "{0}{1}/".format(repos.rlw(), slack_ver())
        elif self.repo == "alien":
            lib = lib_path + "alien_repo/PACKAGES.TXT"
            self.mirror = repos.alien()
            self.step = self.step * 2
        elif self.repo == "slacky":
            lib = lib_path + "slacky_repo/PACKAGES.TXT"
            arch = ""
            if os.uname()[4] == "x86_64":
                arch = "64"
            self.mirror = "{0}slackware{1}-{2}/".format(repos.slacky(), arch,
                                                        slack_ver())
            self.step = self.step * 2
        f = open(lib, "r")
        self.PACKAGES_TXT = f.read()
        f.close()
        sys.stdout.write("{0}Done{1}\n".format(color['GREY'], color['ENDC']))

    def repo_init(self):
        '''
        Initialization repository if only use
        '''
        # initialization Slackware repository needed to compare
        # slacky dependencies
        if not os.path.isfile(lib_path + "slack_repo/PACKAGES.TXT"):
            Initialization().slack()
        repository = {
            "rlw": Initialization().rlw,
            "alien": Initialization().alien,
            "slacky": Initialization().slacky
        }
        repository[self.repo]()

    def start(self):
        '''
        Install packages from official Slackware distribution
        '''
        try:
            dependencies = resolving_deps(self.package, self.repo)
            (dwn_links, install_all, comp_sum, uncomp_sum,
                matching) = self.store(dependencies)
            sys.stdout.write("{0}Done{1}\n".format(color['GREY'],
                                                   color['ENDC']))
            print("")   # new line at start
            if install_all:
                template(78)
                print("{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}".format(
                    "| Package", " " * 17,
                    "Version", " " * 12,
                    "Arch", " " * 4,
                    "Build", " " * 2,
                    "Repos", " " * 10,
                    "Size"))
                template(78)
                if not matching:
                    print("Installing:")
                    sums = views(install_all, comp_sum, self.repo, dependencies)
                    unit, size = units(comp_sum, uncomp_sum)
                    msg = msgs(install_all, sums[2])
                    print("\nInstalling summary")
                    print("=" * 79)
                    print("{0}Total {1} {2}.".format(color['GREY'],
                                                     len(install_all), msg[0]))
                    print("{0} {1} will be installed, {2} will be upgraded and "
                          "{3} will be resettled.".format(sums[2], msg[1],
                                                          sums[1], sums[0]))
                    print("Need to get {0} {1} of archives.".format(size[0],
                                                                    unit[0]))
                    print("After this process, {0} {1} of additional disk "
                          "space will be used.{2}".format(size[1], unit[1],
                                                          color['ENDC']))
                    if default_answer == "y":
                        answer = default_answer
                    else:
                        answer = raw_input("\nWould you like to continue " +
                                           "[Y/n]? ")
                    if answer in ['y', 'Y']:
                        install_all.reverse()
                        packages_dwn(self.tmp_path, dwn_links)
                        install(self.tmp_path, install_all)
                        write_deps(dependencies)
                        delete(self.tmp_path, install_all)
                else:
                    print("Matching:")
                    sums = views(install_all, comp_sum, self.repo, dependencies)
                    msg = msgs(install_all, sums[2])
                    print("\nInstalling summary")
                    print("=" * 79)
                    print("{0}Total found {1} matching {2}.".format(
                        color['GREY'], len(install_all), msg[1]))
                    print("{0} installed {1} and {2} uninstalled {3}.{4}"
                          "\n".format(sums[0] + sums[1], msg[0], sums[2],
                                      msg[1], color['ENDC']))
            else:
                pkg_not_found("", self.package, "No matching", "\n")
        except KeyboardInterrupt:
            print("")   # new line at exit
            sys.exit()

    def store(self, deps):
        '''
        Store and return packages for install
        '''
        dwn, install, comp_sum, uncomp_sum = ([] for i in range(4))
        black = BlackList().packages()
        matching = False
        # name = data[0]
        # location = data[1]
        # size = data[2]
        # unsize = data[3]
        data = repo_data(self.PACKAGES_TXT, self.step, self.repo, self.version)
        if len(deps) > 1:
            for pkg in deps:
                for name, loc, comp, uncomp in zip(data[0], data[1], data[2],
                                                   data[3]):
                    if name.startswith(pkg + "-") and pkg not in black:
                        # store downloads packages by repo
                        dwn.append("{0}{1}/{2}".format(self.mirror, loc, name))
                        install.append(name)
                        comp_sum.append(comp)
                        uncomp_sum.append(uncomp)
        else:
            for name, loc, comp, uncomp in zip(data[0], data[1], data[2],
                                               data[3]):
                package = "".join(deps)
                if package in name and package not in black:
                    # store downloads packages by repo
                    dwn.append("{0}{1}/{2}".format(self.mirror, loc, name))
                    install.append(name)
                    comp_sum.append(comp)
                    uncomp_sum.append(uncomp)
                    if len(install) > 1:
                        matching = True
        dwn.reverse()
        install.reverse()
        comp_sum.reverse()
        uncomp_sum.reverse()
        return [dwn, install, comp_sum, uncomp_sum, matching]


def views(install_all, comp_sum, repository, dependencies):
    '''
    Views packages
    '''
    count = pkg_sum = uni_sum = upg_sum = 0
    # fix repositories align
    align = {
        "rlw": ' ' * 3,
        "alien": ' ',
        "slacky": ''
    }
    repository += align[repository]
    for pkg, comp in zip(install_all, comp_sum):
        pkg_split = split_package(pkg[:-4])
        if find_package(pkg_split[0] + "-" + pkg_split[1], pkg_path):
            pkg_sum += 1
            COLOR = color['GREEN']
        elif find_package(pkg_split[0] + "-", pkg_path):
            COLOR = color['YELLOW']
            upg_sum += 1
        else:
            COLOR = color['RED']
            uni_sum += 1
        print(" {0}{1}{2}{3}{4}{5}{6}{7}{8}{9}{10}{11:>11}{12}".format(
            COLOR, pkg_split[0], color['ENDC'],
            " " * (25-len(pkg_split[0])), pkg_split[1],
            " " * (19-len(pkg_split[1])), pkg_split[2],
            " " * (8-len(pkg_split[2])), pkg_split[3],
            " " * (7-len(pkg_split[3])), repository,
            comp, " K"))
        if len(dependencies) > 1 and len(install_all) > 1 and count == 0:
            print("Installing for dependencies:")
        count += 1
    return [pkg_sum, upg_sum, uni_sum]


def msgs(install_all, uni_sum):
    '''
    Print singular plural
    '''
    msg_pkg = "package"
    msg_2_pkg = msg_pkg
    if len(install_all) > 1:
        msg_pkg = msg_pkg + "s"
    if uni_sum > 1:
        msg_2_pkg = msg_2_pkg + "s"
    return [msg_pkg, msg_2_pkg]


def install(tmp_path, install_all):
    '''
    Install or upgrade packages
    '''
    for install in install_all:
        package = (tmp_path + install).split()
        if os.path.isfile(pkg_path + install[:-4]):
            print("[ {0}reinstalling{1} ] --> {2}".format(color['GREEN'],
                                                          color['ENDC'],
                                                          install))
            PackageManager(package).reinstall()
        elif find_package(split_package(install)[0] + "-", pkg_path):
            print("[ {0}upgrading{1} ] --> {2}".format(color['YELLOW'],
                                                       color['ENDC'],
                                                       install))
            PackageManager(package).upgrade()
        else:
            print("[ {0}installing{1} ] --> {2}".format(color['GREEN'],
                                                        color['ENDC'],
                                                        install))
            PackageManager(package).upgrade()


def resolving_deps(name, repo):
    '''
    Return package dependencies
    '''
    requires, dependencies = [], []
    sys.stdout.write("{0}Resolving dependencies ...{1}".format(color['GREY'],
                                                               color['ENDC']))
    sys.stdout.flush()
    deps = dependencies_pkg(name, repo)
    requires.append(name)
    # Create one list for all packages
    for pkg in deps:
        requires += pkg
    requires.reverse()
    # Remove double dependencies
    for duplicate in requires:
        if duplicate not in dependencies:
            dependencies.append(duplicate)
    return dependencies


def write_deps(dependencies):
    '''
    Write dependencies in a log file
    into directory `/var/log/slpkg/dep/`
    '''
    name = dependencies[-1]
    if find_package(name + "-", pkg_path):
        dep_path = log_path + "dep/"
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        if not os.path.exists(dep_path):
            os.mkdir(dep_path)
        if os.path.isfile(dep_path + name):
            os.remove(dep_path + name)
        if len(dependencies[:-1]) > 0:
            with open(dep_path + name, "w") as f:
                for dep in dependencies[:-1]:
                    f.write(dep + "\n")
                f.close()
