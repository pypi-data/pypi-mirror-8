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
import os

from bakery_lint.base import BakeryTestCase as TestCase
from bakery_cli.pifont import PiFont
from bakery_cli.utils import UpstreamDirectory

class TestDiacritic(TestCase):
    """ These tests are using text file with contents of diacritics glyphs """

    name = __name__
    targets = ['upstream-repo']
    tool = 'lint'

    def setUp(self):
        path = os.path.realpath(os.path.dirname(__file__))
        content = open(os.path.join(path, 'diacritics.txt')).read()
        self.diacriticglyphs = [x.strip() for x in content.split() if x.strip()]
        self.directory = UpstreamDirectory(self.operator.path)

    def is_diacritic(self, glyphname):
        for diacriticglyph in self.diacriticglyphs:
            if glyphname.find(diacriticglyph) >= 1:
                return True

    def filter_diacritics_glyphs(self):
        diacritic_glyphs = []
        for filepath in self.directory.UFO:
            pifont = PiFont(os.path.join(self.operator.path, filepath))
            for glyphcode, glyphname in pifont.get_glyphs():
                if not self.is_diacritic(glyphname):
                    continue
                diacritic_glyphs.append(pifont.get_glyph(glyphname))
        return diacritic_glyphs

    def test_diacritic_made_as_own_glyphs(self):
        """ Check that diacritic glyph are made completely with flat method """
        diacritic_glyphs = self.filter_diacritics_glyphs()

        flatglyphs = 0
        for glyph in diacritic_glyphs:
            if glyph.contours and not glyph.components and not glyph.anchors:
                flatglyphs += 1

        if flatglyphs and len(diacritic_glyphs) != flatglyphs:
            percentage = flatglyphs * 100. / len(diacritic_glyphs)
            self.fail('%.2f%% are made by Flat' % percentage)

    def test_diacritic_made_as_component(self):
        """ Check that diacritic glyph are made completely with composite """
        diacritic_glyphs = self.filter_diacritics_glyphs()

        compositeglyphs = 0
        for glyph in diacritic_glyphs:
            if glyph.components:
                compositeglyphs += 1

        if compositeglyphs and len(diacritic_glyphs) != compositeglyphs:
            percentage = compositeglyphs * 100. / len(diacritic_glyphs)
            self.fail('%.2f%% are made by Composite' % percentage)

    def test_diacritic_made_as_mark_to_mark(self):
        """ Check that diacritic glyph are made completely with mark method """
        diacritic_glyphs = self.filter_diacritics_glyphs()

        markglyphs = 0
        for glyph in diacritic_glyphs:
            if glyph.anchors:
                markglyphs += 1

        if markglyphs and len(diacritic_glyphs) != markglyphs:
            percentage = markglyphs * 100. / len(diacritic_glyphs)
            self.fail('%.2f%% are made by Mark' % percentage)
