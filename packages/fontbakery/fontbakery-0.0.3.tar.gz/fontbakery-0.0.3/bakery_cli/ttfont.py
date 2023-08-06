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
import re
import os.path as op

from fontTools import ttLib


class BaseFont(object):

    @staticmethod
    def get_ttfont(path):
        return Font(path)

    @staticmethod
    def get_ttfont_from_metadata(path, font_metadata, is_menu=False):
        path = op.join(op.dirname(path), font_metadata.filename)
        if is_menu:
            path = path.replace('.ttf', '.menu')
        return Font.get_ttfont(path)


class Font(BaseFont):

    def __init__(self, fontpath):
        if fontpath[-4:] == '.ttx':
            self.ttfont = ttLib.TTFont(None)
            self.ttfont.importXML(fontpath, quiet=True)
        else:
            self.ttfont = ttLib.TTFont(fontpath)

        self.ascents = AscentGroup(self.ttfont)
        self.descents = DescentGroup(self.ttfont)
        self.linegaps = LineGapGroup(self.ttfont)

    def __getitem__(self, key):
        """ Returns TTFont table with key name

        >>> font = Font("tests/fixtures/ttf/Font-Bold.ttf")
        >>> font['name'].tableTag
        'name'
        """
        return self.ttfont[key]

    def get_program_bytecode(self):
        """ Return binary program code from "prep" table.

        >>> font = Font("tests/fixtures/ttf/Font-Bold.ttf")
        >>> font.get_program_bytecode()
        '\\xb8\\x01\\xff\\x85\\xb0\\x04\\x8d'
        """
        try:
            return self['prep'].program.getBytecode()
        except KeyError:
            return ""

    def get_bounding(self):
        """ Returns max and min bbox font

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.get_bounding()
        (-384, 1178)
        """
        if self.ttfont.sfntVersion == 'OTTO':
            return self['head'].yMin, self['head'].yMax

        ymax = 0
        for g in self['glyf'].glyphs:
            char = self['glyf'][g]
            if hasattr(char, 'yMax') and ymax < char.yMax:
                ymax = char.yMax

        ymin = 0
        for g in self['glyf'].glyphs:
            char = self['glyf'][g]
            if hasattr(char, 'yMin') and ymin > char.yMin:
                ymin = char.yMin

        return ymin, ymax

    @property
    def license_url(self):
        """ Return LicenseURL from "name" table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.license_url
        u'http://scripts.sil.org/OFL'
        """
        for name in self.names:
            if name.nameID == 14:
                return Font.bin2unistring(name)

    @property
    def macStyle(self):
        return self['head'].macStyle

    @property
    def italicAngle(self):
        return self['post'].italicAngle

    @property
    def names(self):
        return self['name'].names

    @property
    def glyphs(self):
        """ Returns list of glyphs names in fonts

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(len(font.glyphs))
        502
        """
        return self.ttfont.getGlyphOrder()

    @property
    def OS2_usWeightClass(self):
        """ OS/2.usWeightClass property value

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.OS2_usWeightClass)
        400
        """
        return self['OS/2'].usWeightClass

    @property
    def OS2_usWidthClass(self):
        """ Returns OS/2.usWidthClass property value

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.OS2_usWidthClass
        5
        """
        return self['OS/2'].usWidthClass

    @property
    def OS2_fsType(self):
        """ OS/2.fsType property value

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.OS2_fsType)
        8
        """
        return self['OS/2'].fsType

    def platform_entry(self, entry):
        if entry.platformID == 1 and entry.langID == 0:
            return Font.bin2unistring(entry)
        elif entry.platformID == 3 and entry.langID == 0x409:
            return Font.bin2unistring(entry)


    @property
    def fullname(self):
        """ Returns fullname of fonts

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.fullname
        u'Monda Regular'
        """
        for entry in self.names:
            if entry.nameID != 4:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    @property
    def _style_name(self):
        for entry in self.names:
            if entry.nameID != 2:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    @property
    def stylename(self):
        """ Returns OpenType specific style name

        >>> font = Font("tests/fixtures/ttf/Font-Bold.ttf")
        >>> font.stylename
        u'Bold'
        """
        return self._style_name

    @property
    def _family_name(self):

        for entry in self.names:
            if entry.nameID != 1:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    @property
    def familyname(self):
        """ Returns fullname of fonts

        >>> font = Font("tests/fixtures/ttf/Font-Bold.ttf")
        >>> font.familyname
        u'Font'
        """
        return self._family_name

    @property
    def ot_family_name(self):
        """ Returns Windows-only Opentype-specific FamilyName """
        for entry in self.names:
            # This value must be only for windows platform as in
            # mac it addresses some problems with installing fonts with
            # that ids
            if entry.nameID != 16 or entry.platformID != 3:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    @property
    def ot_style_name(self):
        """ Returns Windows-only Opentype-specific StyleName """
        for entry in self.names:
            # This value must be only for windows platform as in
            # mac it addresses some problems with installing fonts with
            # that ids
            if entry.nameID != 17 or entry.platformID != 3:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    @property
    def ot_full_name(self):
        """ Returns Windows-only Opentype-specific FullName """
        for entry in self.names:
            # This value must be only for windows platform as in
            # mac it addresses some problems with installing fonts with
            # that ids
            if entry.nameID != 18 or entry.platformID != 3:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    @property
    def post_script_name(self):
        """ Returns fullname of fonts

        >>> font = Font("tests/fixtures/ttf/Font-Bold.ttf")
        >>> font.post_script_name
        u'Font-Bold'
        """
        for entry in self.names:
            if entry.nameID != 6:
                continue
            value = self.platform_entry(entry)
            if value:
                return value
        return ''

    def retrieve_cmap_format_4(self):
        """ Returns cmap table format 4

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.retrieve_cmap_format_4().platEncID)
        3
        """
        for cmap in self['cmap'].tables:
            if cmap.format == 4:
                return cmap

    def advance_width(self, glyph_id=None):
        """ AdvanceWidth of glyph from "hmtx" table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.advance_width("a"))
        572
        """
        if not glyph_id:
            return self['hhea'].advanceWidthMax
        try:
            return self['hmtx'].metrics[glyph_id][0]
        except KeyError:
            return None

    @staticmethod
    def bin2unistring(record):
        if b'\000' in record.string:
            return record.string.decode('utf-16-be')
        elif not isinstance(record.string, unicode):
            return unicode(record.string, 'unicode_escape')
        return record.string

    def get_glyf_length(self):
        """ Length of "glyf" table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.get_glyf_length())
        21804
        """
        return self.ttfont.reader.tables['glyf'].length

    def get_loca_length(self):
        """ Length of "loca" table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.get_loca_length())
        1006
        """
        return self.ttfont.reader.tables['loca'].length

    def get_loca_glyph_offset(self, num):
        """ Retrieve offset of glyph in font tables

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.get_loca_glyph_offset(15))
        836
        >>> int(font.get_loca_glyph_offset(16))
        904
        """
        return self['loca'].locations[num]

    def get_loca_glyph_length(self, num):
        """ Retrieve length of glyph in font loca table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> int(font.get_loca_glyph_length(15))
        68
        """
        return self.get_loca_glyph_offset(num + 1) - self.get_loca_glyph_offset(num)

    def get_loca_num_glyphs(self):
        """ Retrieve number of glyph in font loca table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.get_loca_num_glyphs()
        503
        """
        return len(self['loca'].locations)

    def get_hmtx_max_advanced_width(self):
        """ AdvanceWidthMax from "hmtx" table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.get_hmtx_max_advanced_width()
        1409
        """
        advance_width_max = 0
        for g in self['hmtx'].metrics.values():
            advance_width_max = max(g[0], advance_width_max)
        return advance_width_max

    @property
    def advance_width_max(self):
        """ AdvanceWidthMax from "hhea" table

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.advance_width_max
        1409
        """
        return self.advance_width()

    def get_upm_height(self):
        return self['head'].unitsPerEm

    def get_highest_and_lowest(self):
        high = []
        low = []
        if self.ttfont.sfntVersion == 'OTTO':
            return high, low
        maxval = self.ascents.get_max()
        minval = self.descents.get_min()
        for glyph, params in self['glyf'].glyphs.items():
            if hasattr(params, 'yMax') and params.yMax > maxval:
                high.append(glyph)
            if hasattr(params, 'yMin') and params.yMin < minval:
                low.append(glyph)
        return high, low

    def save(self, fontpath):
        self.ttfont.save(fontpath)


def is_none_protected(func):

    def f(self, value):
        if value is None:
            return
        func(self, value)

    return f


class AscentGroup(object):

    def __init__(self, ttfont):
        self.ttfont = ttfont

    def set(self, value):
        self.hhea = value
        self.os2typo = value
        self.os2win = value

    def get_max(self):
        """ Returns largest value of ascents

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.ascents.get_max()
        1178
        """
        return max(self.hhea, self.os2typo, self.os2win)

    def hhea():
        doc = """Ascent value in 'Horizontal Header' (hhea.ascent)

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.ascents.hhea
        1178
        """

        def fget(self):
            return self.ttfont['hhea'].ascent

        @is_none_protected
        def fset(self, value):
            self.ttfont['hhea'].ascent = value

        return locals()
    hhea = property(**hhea())

    def os2typo():
        doc = """Ascent value in 'Horizontal Header' (OS/2.sTypoAscender)

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.ascents.os2typo
        1178
        """

        def fget(self):
            return self.ttfont['OS/2'].sTypoAscender

        @is_none_protected
        def fset(self, value):
            self.ttfont['OS/2'].sTypoAscender = value

        return locals()
    os2typo = property(**os2typo())

    def os2win():
        doc = """Ascent value in 'Horizontal Header' (OS/2.usWinAscent)

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.ascents.os2win
        1178
        """

        def fget(self):
            return self.ttfont['OS/2'].usWinAscent

        @is_none_protected
        def fset(self, value):
            self.ttfont['OS/2'].usWinAscent = value

        return locals()
    os2win = property(**os2win())


class DescentGroup(object):

    def __init__(self, ttfont):
        self.ttfont = ttfont

    def set(self, value):
        self.hhea = value
        self.os2typo = value
        self.os2win = value

    def get_min(self):
        """ Returns least value of descents.

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.descents.get_min()
        -384
        """
        return min(self.hhea, self.os2typo, self.os2win)

    def hhea():
        doc = """ Descent value in 'Horizontal Header' (hhea.descent)

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.descents.hhea
        -384
        """

        def fget(self):
            return self.ttfont['hhea'].descent

        @is_none_protected
        def fset(self, value):
            self.ttfont['hhea'].descent = value

        return locals()
    hhea = property(**hhea())

    def os2typo():
        doc = """Descent value in 'Horizontal Header' (OS/2.sTypoDescender)

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.descents.os2typo
        -384
        """

        def fget(self):
            return self.ttfont['OS/2'].sTypoDescender

        @is_none_protected
        def fset(self, value):
            self.ttfont['OS/2'].sTypoDescender = value

        return locals()
    os2typo = property(**os2typo())

    def os2win():
        doc = """Descent value in 'Horizontal Header' (OS/2.usWinDescent)

        >>> font = Font("tests/fixtures/ttf/Font-Regular.ttf")
        >>> font.descents.os2win
        384
        """

        def fget(self):
            return self.ttfont['OS/2'].usWinDescent

        @is_none_protected
        def fset(self, value):
            self.ttfont['OS/2'].usWinDescent = abs(value)

        return locals()
    os2win = property(**os2win())


class LineGapGroup(object):

    def __init__(self, ttfont):
        self.ttfont = ttfont

    def set(self, value):
        self.hhea = value
        self.os2typo = value

    def hhea():
        doc = "The hhea.lineGap property"

        def fget(self):
            return self.ttfont['hhea'].lineGap

        @is_none_protected
        def fset(self, value):
            self.ttfont['hhea'].lineGap = value

        return locals()
    hhea = property(**hhea())

    def os2typo():
        doc = "The OS/2.sTypoLineGap property"

        def fget(self):
            return self.ttfont['OS/2'].sTypoLineGap

        @is_none_protected
        def fset(self, value):
            self.ttfont['OS/2'].sTypoLineGap = value

        return locals()
    os2typo = property(**os2typo())


class FontTool:

    @staticmethod
    def get_tables(path):
        """ Retrieves tables names existing in font

        >>> FontTool.get_tables("tests/fixtures/ttf/Font-Regular.ttf")
        ['GDEF', 'gasp', 'loca', 'name', 'post', 'OS/2', 'maxp', 'head', \
'kern', 'FFTM', 'GSUB', 'glyf', 'GPOS', 'cmap', 'hhea', 'hmtx', 'DSIG']
        """
        font = ttLib.TTFont(path)
        return font.reader.tables.keys()


def getName(font, pairs):
    value = None
    for pair in pairs:
        value = font['name'].getName(*pair)
        if value:
            break

    if value.isUnicode():
        value = value.string.decode('utf-16-be')
    else:
        value = value.string

    assert value, u'{} seems to be missed in NAME table'.format(pairs)
    return value


def getSuggestedFontNameValues(font):
    family_name = getName(font, [[1, 3, 1],
                                 [1, 1, 0]])

    subfamily_name = getName(font, [[2, 3, 1],
                                    [2, 1, 0]])

    full_name = getName(font, [[4, 3, 1],
                               [4, 1, 0]])

    subfamilies = ['Regular',
                   'Bold',
                   'Italic',
                   'Semi Bold Italic',
                   'Semi Bold',
                   'Heavy',
                   'Heavy Italic',
                   'Extra Light Italic',
                   'Extra Light',
                   'Medium',
                   'Extra Bold',
                   'Medium Italic',
                   'Extra Bold Italic',
                   'Bold Italic',
                   'Thin Italic',
                   'Thin',
                   'Light Italic',
                   'Light',
                   'Black',
                   'Black Italic']

    if full_name == family_name:
        try:
            family_name, subfamily_name = full_name.split(' ', 1)[:]
        except ValueError:
            pass

    if subfamily_name == 'Normal' or subfamily_name == 'Roman':
        subfamily_name = 'Regular'
    elif subfamily_name == 'Heavy':
        subfamily_name = 'Black'
    elif subfamily_name == 'Heavy Italic':
        subfamily_name = 'Black Italic'
    return {'family': family_name, 'subfamily': subfamily_name}
