#!/usr/bin/env python2
# -*- python -*-
#BEGIN_LEGAL
#
#Copyright (c) 2018 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#  
#END_LEGAL
from __future__ import print_function
import os
import sys
import argparse
import re
import collections

import read_xed_db

def die(s):
    sys.stdout.write("ERROR: {0}\n".format(s))
    sys.exit(1)
def msgb(b,s=''):
    sys.stdout.write("[{0}] {1}\n".format(b,s))



def work(args):  # main function
    msgb("READING XED DB")


    xeddb = read_xed_db.xed_reader_t(args.state_bits_filename,
                                     args.instructions_filename,
                                     args.widths_filename,
                                     args.element_types_filename)

    histo = collections.defaultdict(int)
    for r in xeddb.recs:
        if hasattr(r,'operands'):
            s = re.sub(r'[ ]+',' ',r.operands)
            if 0:
                histo[s] = histo[s] + 1
            if 1:
                for t in s.split():
                    if t.startswith('REG'):
                        t = 'REG' + t[4:]
                    if t.startswith('MEM'):
                        t = 'MEM' + t[4:]
                    histo[t] = histo[t] + 1
        


    for k,v in sorted( list(histo.items()), key=lambda t: t[1] ):
        print("{0:4d} {1}".format(v,k))
    print("TOTAL: ", len(histo))

    return 0


def setup():
    parser = argparse.ArgumentParser(
        description='Generate instruction counts per chip')
    parser.add_argument('state_bits_filename', 
                        help='Input state bits file')
    parser.add_argument('instructions_filename', 
                        help='Input instructions file')
    parser.add_argument('widths_filename', 
                        help='Input chip file')
    parser.add_argument('element_types_filename', 
                        help='Input chip file')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = setup()
    r = work(args)
    sys.exit(r)

