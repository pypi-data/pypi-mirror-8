#
# Copyright (c) 2014 LexisNexis Risk Data Management Inc.
#
# This file is part of the RadSSH software package.
#
# RadSSH is free software, released under the Revised BSD License.
# You are permitted to use, modify, and redsitribute this software
# according to the Revised BSD License, a copy of which should be
# included with the distribution as file LICENSE.txt
#

'''
RadSSH - SSH parallel pseudo-shell and toolkit
'''

from __future__ import print_function  # Requires Python 2.6 or higher

_svn_info = "$Id: __init__.py 5239 2014-12-03 16:07:48Z paul $"

version_info = (1, 0, 0)
version = '.'.join([str(x) for x in version_info])

__author__ = 'Paul Kapp'
__author_email__ = 'paul.kapp@risk.lexisnexis.com'

if __name__ == '__main__':
    print('API module can not be run')
