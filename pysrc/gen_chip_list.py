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
import chipmodel

def die(s):
    sys.stdout.write("ERROR: {0}\n".format(s))
    sys.exit(1)
def msgb(b,s=''):
    sys.stdout.write("[{0}] {1}\n".format(b,s))


def check(chip, xeddb, chipdb, classes):
    icount = 0
    histo = collections.defaultdict(int)
    for inst in xeddb.recs:
        if inst.isa_set in chipdb[chip]:
            icount = icount + 1
            clas = classes[inst.isa_set]
            if inst.scalar:
                clas = clas + '.sc'
            histo[clas] = histo[clas] + 1
    return (chip, icount, histo)



def work(args):  # main function
    msgb("READING XED DB")
    (chips, chip_db) = chipmodel.read_database(args.chip_filename)

    xeddb = read_xed_db.xed_reader_t(args.state_bits_filename,
                                     args.instructions_filename,
                                     args.widths_filename,
                                     args.element_types_filename)

    isasets = set()
    for r in xeddb.recs:
        isasets.add(r.isa_set)

    classes = {}
    for i in isasets:
        c = 'general'
        if 'XOP' in i:
            c = 'xop'
        elif 'SSE' in i:
            c = 'sse'
        elif 'AVX512' in i:
            c = 'avx512'
        elif 'ICL' in i:
            c = 'avx512'
        elif 'AVX' in i:
            c = 'avx'
        elif 'FMA' in i:
            c = 'avx'
        elif 'F16C' in i:
            c = 'avx'
        elif 'MMX' in i:
            c = 'mmx'
        classes[i]=c

    all = []
    for c in chips:
        r = check(c, xeddb, chip_db, classes)
        all.append(r)

    groups = [ 'general', 'mmx', 'sse', 'avx', 'avx512' ]

    for inst in xeddb.recs:
        if classes[inst.isa_set] == 'general' and inst.scalar:
            print("GPR SCALAR", inst.iclass)

    tlist = []
    for s in all:
        t = []
        (chip, icount, histo) = s
        t.append("{0:20s} {1:4d}".format(chip,icount))
        for scalar in ['.sc', '']:
            for x in groups:
                k = x + scalar
                t.append( "{0:7s}:{1:4d}".format( k, histo[k]))
        tlist.append((icount, " ".join(t)))
    def keyfn(x):
        return x[0]
    tlist.sort(key=keyfn)

    for x,y in tlist:
        print(y)

    return 0


def setup():
    parser = argparse.ArgumentParser(
        description='Generate instruction counts per chip')
    parser.add_argument('state_bits_filename', 
                        help='Input state bits file')
    parser.add_argument('instructions_filename', 
                        help='Input instructions file')
    parser.add_argument('chip_filename', 
                        help='Input chip file')
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

