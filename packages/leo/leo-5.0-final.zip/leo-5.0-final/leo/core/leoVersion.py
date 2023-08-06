#@+leo-ver=5-thin
#@+node:ekr.20090717092906.12765: * @file leoVersion.py
'''A module holding version-related info.'''
import os
import json
#@+<< version dates >>
#@+node:ekr.20141117073519.12: ** << version dates >>
#@@nocolor-node
#@+at
# Leo 4.5.1 final: September 14, 2008
# Leo 4.6.1 final: July 30, 2009.
# Leo 4.7.1 final: February 26, 2010.
# Leo 4.8   final: November 26, 2010.
# Leo 4.9   final: June 21, 2011.
# Leo 4.10  final: March 29, 2012.
# Leo 4.11 a1: August 18, 2013
# Leo 4.11 a2: August 19, 2013
# Leo 4.11 b1: October 31, 2013
# Leo 4.11 final: November 6, 2013
# Leo 5.0 a1: November 6, 2014
# Leo 5.0 a2: November 8, 2014
# Leo 5.0 b1: November 13, 2014
# Leo 5.0 b2: November 17, 2014
# Leo 5.0 final: November 24, 2014
#@-<< version dates >>

# get info from leo/core/commit_timestamp.json
leo_core_path = os.path.dirname(os.path.realpath(__file__))
    # leoVersion.py is in leo/core
commit_path = os.path.join(leo_core_path, 'commit_timestamp.json')
commit_info = json.load(open(commit_path))
commit_timestamp = commit_info['timestamp']
commit_asctime = commit_info['asctime']

version = "5.0-final" # Used if no git version is available.

# attempt to grab commit + branch info from git, else ignore it
git_info = {}
theDir = os.path.dirname(__file__)
path = os.path.join(theDir,'..','..','.git','HEAD')
if os.path.exists(path):
    s = open(path,'r').read()
    if s.startswith('ref'):
        # on a proper branch
        pointer = s.split()[1]
        dirs = pointer.split('/')
        branch = dirs[-1]
        path = os.path.join(theDir, '..', '..', '.git', pointer)
        s = open(path, 'r').read().strip()[0:12]
            # shorten the hash to a unique shortname 
            # (12 characters should be enough until the end of time, for Leo...)
        git_info['branch'] = branch
        git_info['commit'] = s
    else:
        branch = 'None'
        s = s[0:12]
        git_info['branch'] = branch
        git_info['commit'] = s

build = commit_timestamp
date = commit_asctime
#@@language python
#@@tabwidth -4
#@-leo
