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
from bakery_lint.base import BakeryTestCase as TestCase, tags, autofix
from bakery_cli.ttfont import Font

from bakery_cli.scripts.nbsp import getGlyph, getWidth


class CheckNbspWidthMatchesSpWidth(TestCase):

    targets = ['result']
    tool = 'lint'
    name = __name__

    @tags('required')
    @autofix('bakery_cli.pipe.autofix.fix_nbsp')
    def test_check_nbsp_width_matches_sp_width(self):
        """ Check non-breaking space's advancewidth is the same as space """
        tf = Font.get_ttfont(self.operator.path)

        space = getGlyph(tf.ttfont, 0x0020)
        nbsp = getGlyph(tf.ttfont, 0x00A0)

        _ = "Font does not contain a space glyph"
        self.assertTrue(space, _)
        _ = "Font does not contain a nbsp glyph"
        self.assertTrue(nbsp, _)

        _ = ("The nbsp advance width does not match "
             "the space advance width")

        spaceWidth = getWidth(tf.ttfont, space)
        nbspWidth = getWidth(tf.ttfont, nbsp)
        self.assertEqual(spaceWidth, nbspWidth, _)
