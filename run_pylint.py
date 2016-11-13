#!/usr/bin/env python
# ref: https://gist.github.com/gregorynicholas/3152237
'''
Module that runs pylint on all python scripts found in a directory tree.
'''

import os
import sys

def check(module):
    '''
    apply pylint to the file specified if it is a *.py file
    '''

    if module[-3:] == ".py":
        print("CHECKING ", module)
        pout = os.popen('pylint %s'% module, 'r')
        if pout:
            for line in pout:
                if not "*" in line:
                    print(line, end="")

if __name__ == "__main__":
    try:
        # print(sys.argv)
        BASE_DIRECTORY = sys.argv[1]
    except IndexError:
        BASE_DIRECTORY = os.getcwd()

    print("linting *.py files beneath \n  {0}".format(BASE_DIRECTORY))
    print("=" * 80)
    for root, dirs, files in os.walk(BASE_DIRECTORY):
        for name in files:
            filepath = os.path.join(root, name)
            check(filepath)

    print("=" * 80)
