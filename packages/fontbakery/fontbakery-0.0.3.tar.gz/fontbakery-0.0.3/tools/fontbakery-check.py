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
import sys

from bakery_lint.base import tests_report
from bakery_lint import run_set


available_tests = ['result', 'upstream', 'upstream-ttx', 'metadata',
                   'description', 'upstream-repo']


if __name__ == '__main__':
    description = 'Runs checks or tests on specified directory/file(s)'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('test', help="Action or target test suite",
                        choices=['*', 'list'] + available_tests)
    parser.add_argument('file', nargs="+", help="Test files, can be a list")
    parser.add_argument('--verbose', '-v', action='count',
                        help="Verbosity level", default=1)

    args = parser.parse_args()
    if args.test == 'list':
        tests_report()
        sys.exit()

    if not args.file:
        print("Missing files to test", file=sys.stderr)
        sys.exit(1)

    for x in args.file:
        failures = []
        success = []
        error = []
        tests = [args.test]

        if args.test == '*':
            tests = available_tests

        for test in tests:
            result = run_set(x, test)
            failures += [(x._testMethodName, x._err_msg)
                        for x in result.get('failure', [])]
            error += [(x._testMethodName, x._err_msg)
                     for x in result.get('error', [])]
            success += [(x._testMethodName, 'OK')
                       for x in result.get('success', [])]

        if not bool(failures + error):
            print('OK')
        else:
            import pprint
            _pprint = pprint.PrettyPrinter(indent=4)
            _pprint.pprint(failures + error + success)
