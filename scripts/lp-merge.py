#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2015 OpenLP Developers                                   #
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
This script is used by developers to merge branches from launchpad.net into
other branches, which is basically what happens every time a merge proposal
is merged into trunk. This script simplifies the process and helps avoiding
merging to the wrong branch by doing some checks.
For the script to work it is assumed that the developer doing the merging
has a checkout (not branch) of the target branch.

Merge a branch
--------------
Once a branch has been approved for merging, go to the local folder with the
checkout of the target branch, copy the url from the merge proposal on launchpad
and use it like this:

    script/lp-merge.py <url>

The url could look like this:
https://code.launchpad.net/~tomasgroth/openlp/doc22update4/+merge/271874

First you'll be asked whether to merge the branch from the url to the local
branch, which will be done if you answer 'y'. The script checks that the current
folder is the right one before merging.
Then you'll be asked whether to commit the changes to the branch. The script
shows the command it will run, including detected linked bugs and author. If you
wish to change it, you can chose to run 'qcommit', an bzr GUI. Note that you'll
have to install qbzr for this to work. If you choose to run qcommit the script
will print the detected bugs + author for easy copying into the GUI.
"""
import subprocess
import re
import sys
import os
import urllib.request
from bs4 import BeautifulSoup

# Check that the argument count is correct
if len(sys.argv) != 2:
    print('\n\tUsage: ' + sys.argv[0] + ' <url to approved merge request>\n')
    exit()

url = sys.argv[1]
pattern = re.compile('.+?/\+merge/\d+')
match = pattern.match(url)

# Check that the given argument is an url in the right format
if not url.startswith('https://code.launchpad.net/~') or match is None:
    print('The url is not valid! It should look like this:\n    '
          'https://code.launchpad.net/~tomasgroth/openlp/doc22update4/+merge/271874')

page = urllib.request.urlopen(url)
soup = BeautifulSoup(page.read(), 'lxml')

# Find this span tag that contains the branch url
# <span class="branch-url">
span_branch_url = soup.find('span', class_='branch-url')
branch_url = span_branch_url.contents[0]

# Find this tag that describes the branch. We'll use that for commit message
# <meta name="description" content="...">
meta = soup.find('meta', attrs={"name": "description"})

commit_message = meta.get('content')

# Find all tr-tags with this class. Makes it possible to get bug numbers.
# <tr class="bug-branch-summary"
bug_rows = soup.find_all('tr', class_='bug-branch-summary')
bugs = []
for row in bug_rows:
    id_attr = row.get('id')
    bugs.append(id_attr[8:])

# Find target branch name using the tag below
# <div class="context-publication"><h1>Merge ... into...
div_branches = soup.find('div', class_='context-publication')
branches = div_branches.h1.contents[0]
target_branch = '+branch/' + branches[(branches.find(' into lp:') + 9):]

# Check that we are in the right branch
bzr_info_output = subprocess.check_output(['bzr', 'info'])
if target_branch not in bzr_info_output.decode():
    print('ERROR: It seems you are not in the right folder...')
    exit()

# Find the authors email address. It is hidden in a javascript line like this:
# conf = {"status_value": "Needs review", "source_revid": "tomasgroth@yahoo.dk-20150921204550-gxduegmcmty9rljf",
#         "user_can_edit_status": false, ...
script_tag = soup.find('script', attrs={"id": "codereview-script"})
content = script_tag.contents[0]
start_pos = content.find('source_revid') + 16
pattern = re.compile('.*\w-\d\d\d\d\d+')
match = pattern.match(content[start_pos:])
author_email = match.group()[:-15]

# Merge the branch
do_merge = input('Merge ' + branch_url + ' into local branch? (y/N/q): ').lower()
if do_merge == 'y':
    subprocess.call(['bzr', 'merge', branch_url])
elif do_merge == 'q':
    exit()

# Create commit command
commit_command = ['bzr', 'commit']

for bug in bugs:
    commit_command.append('--fixes')
    commit_command.append('lp:' + bug)

commit_command.append('-m')
commit_command.append(commit_message)

commit_command.append('--author')
commit_command.append('"' + author_email + '"')

print('About to run the bzr command below:\n')
print(' '.join(commit_command))
do_commit = input('Run the command (y), use qcommit (qcommit) or cancel (C): ').lower()

if do_commit == 'y':
    subprocess.call(commit_command)
elif do_commit == 'qcommit':
    # Setup QT workaround to make qbzr look right on my box
    my_env = os.environ.copy()
    my_env['QT_GRAPHICSSYSTEM'] = 'native'
    # Print stuff that kan be copy/pasted into qbzr GUI
    print('These bugs can be copy/pasted in: lp:' + ' lp:'.join(bugs))
    print('The authors email is: ' + author_email)
    # Run qcommit
    subprocess.call(['bzr', 'qcommit', '-m', commit_message], env=my_env)
