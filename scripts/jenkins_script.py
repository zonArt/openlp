#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
This script helps to trigger builds of branches. To use it you have to install the jenkins-webapi package:

    pip3 install jenkins-webapi

You probably want to create an alias. Add this to your ~/.bashrc file and then logout and login (to apply the alias):

    alias ci="python3 ./scripts/jenkins_script.py TOKEN"

You can look up the token in the Branch-01-Pull job configuration or ask in IRC.
"""

from optparse import OptionParser
import re
from requests.exceptions import HTTPError
from subprocess import Popen, PIPE
import sys
import time

from jenkins import Jenkins


JENKINS_URL = 'http://ci.openlp.org/'
REPO_REGEX = r'(.*/+)(~.*)'


class OpenLPJobs(object):
    """
    This class holds any jobs we have on jenkins and we actually need in this script.
    """
    Branch_Pull = 'Branch-01-Pull'
    Branch_Functional = 'Branch-02-Functional-Tests'
    Branch_Interface = 'Branch-03-Interface-Tests'
    Branch_Windows = 'Branch-04-Windows_Tests'
    Branch_PEP = 'Branch-05-Code-Analysis'
    PEP_TEST = "sdafajsdklfj lajsldfk jlasdkjf lkajdf lkasjdlfkjalskdjflkajflkadsjkfl jasdlkfj laskdjflka sjdlkfjlaksdjflksajdf"

    Jobs = [Branch_Pull, Branch_Functional, Branch_Interface, Branch_Windows, Branch_PEP]


class JenkinsTrigger(object):
    def __init__(self, token):
        """
        Create the JenkinsTrigger instance.

        :param token: The token we need to trigger the build. If you do not have this token, ask in IRC.
        """
        self.token = token
        self.repo_name = get_repo_name()
        self.jenkins_instance = Jenkins(JENKINS_URL)

    def trigger_build(self):
        """
        Ask our jenkins server to build the "Branch-01-Pull" job.
        """
        self.jenkins_instance.job(OpenLPJobs.Branch_Pull).build({'BRANCH_NAME': self.repo_name}, token=self.token)

    def print_output(self):
        """
        Print the status information of the build tirggered.
        """
        print("Add this to your merge proposal:")
        print("--------------------------------")
        for job in OpenLPJobs.Jobs:
            self.__print_build_info(job)

    def open_browser(self):
        """
        Opens the browser.
        """
        url = self.jenkins_instance.job(OpenLPJobs.Branch_Pull).info['url']
        # Open the url
        Popen(('xdg-open', url), stderr=PIPE)

    def __print_build_info(self, job_name):
        """
        This helper method prints the job information of the given ``job_name``

        :param job_name: The name of the job we want the information from. For example *Branch-01-Pull*. Use the class
         variables from the :class:`OpenLPJobs` class.
        """
        job = self.jenkins_instance.job(job_name)
        while job.info['inQueue']:
            time.sleep(1)
        build = job.last_build
        build.wait()
        result_string = build.info['result']
        url = build.info['url']
        print('[%s] %s' % (result_string, url))
        # On failure open the browser.
        #if result_string == "FAILURE":
        #    url += 'console'
        #    Popen(('xdg-open', url), stderr=PIPE)


def get_repo_name():
    """
    This returns the name of branch of the wokring directory. For example it returns *lp:~googol/openlp/render*.
    """
    # Run the bzr command.
    bzr = Popen(('bzr', 'info'), stdout=PIPE, stderr=PIPE)
    raw_output, error = bzr.communicate()
    # Detect any errors
    if error:
        print('This is not a branch.')
        return
    # Clean the output.
    raw_output = raw_output.decode()
    output_list = list(map(str.strip, raw_output.split('\n')))
    # Determine the branch's name
    repo_name = ''
    for line in output_list:
        # Check if it is remote branch.
        if 'push branch' in line:
            match = re.match(REPO_REGEX, line)
            if match:
                repo_name = 'lp:%s' % match.group(2)
                break
        elif 'checkout of branch' in line:
            match = re.match(REPO_REGEX, line)
            if match:
                repo_name = 'lp:%s' % match.group(2)
                break
    repo_name = repo_name.strip('/')

    # Did we find the branch name?
    if not repo_name:
        for line in output_list:
            # Check if the branch was pushed.
            if 'Shared repository with trees (format: 2a)' in line:
                print('Not a branch. cd to a branch.')
                return
        print('Not a branch. Have you pushed it to launchpad?')
        return
    return repo_name


def main():
    usage = 'Usage: python %prog TOKEN [options]'

    parser = OptionParser(usage=usage)
    parser.add_option('-d', '--disable-output', dest='enable_output', action="store_false", default=True,
                      help='Disable output.')
    parser.add_option('-b', '--open-browser', dest='open_browser', action="store_true", default=False,
                      help='Opens the jenkins page in your browser.')
    #parser.add_option('-e', '--open-browser-on-error', dest='open_browser_on_error', action="store_true",
    #                  default=False, help='Opens the jenkins page in your browser in case a test fails.')
    options, args = parser.parse_args(sys.argv)

    if len(args) == 2:
        if not get_repo_name():
            return
        token = args[-1]
        jenkins_trigger = JenkinsTrigger(token)
        try:
            jenkins_trigger.trigger_build()
        except HTTPError as e:
            print("Wrong token.")
            return
        # Open the browser before printing the output.
        if options.open_browser:
            jenkins_trigger.open_browser()
        if options.enable_output:
            jenkins_trigger.print_output()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
