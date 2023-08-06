#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 The Font Bakery Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.
from __future__ import print_function
import argparse
import os
import sys

from bakery_cli.ttfont import Font
from bakery_cli.scripts.fstype import reset_fstype

from fontTools.ttLib import TTLibError


description = 'Fixes TTF fsType to 0'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('ttf_font', nargs='+',
                    help="Font in OpenType (TTF/OTF) format")
parser.add_argument('--autofix', action="store_true",
                    help="Autofix font metrics")

args = parser.parse_args()


for path in args.ttf_font:
    if not os.path.exists(path):
        continue

    if args.autofix:
        reset_fstype(path)
    else:
        try:
            font = Font(path)
        except TTLibError as ex:
            print("ERROR: {0}: {1}".format(path, ex), file=sys.stderr)
            continue
        print('{0}: {1}'.format(path, font.OS2_fsType))
