#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from bzrlib.branch import Branch
 
def get_version(path):
    b = Branch.open_containing(path)[0]
    b.lock_read()
    result = '0.0.0'
    try:
        # Get the branch's latest revision number.
        revno = b.revno()
        # Convert said revision number into a bzr revision id.
        revision_id = b.dotted_revno_to_revision_id((revno,))
        # Get a dict of tags, with the revision id as the key.
        tags = b.tags.get_reverse_tag_dict()
        # Check if the latest
        if revision_id in tags:
            result = tags[revision_id][0]
        else:
            result = '%s-bzr%s' % (sorted(b.tags.get_tag_dict().keys())[-1], revno)
    finally:
        b.unlock()
        return result
 
def get_path():
    if len(sys.argv) > 1:
        return os.path.abspath(sys.argv[1])
    else:
        return os.path.abspath('.')
 
if __name__ == u'__main__':
    path = get_path()
    print get_version(path)

