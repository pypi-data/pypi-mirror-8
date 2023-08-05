# -*- coding: utf-8 -*-
#
# builder.py
#
# Copyright (c) 2013,
# Виталий Волков <hash.3g@gmail.com>
# Dave Crossland <dave@understandinglimited.com>
#
# Released under the GNU General Public License version 3 or later.
# See accompanying LICENSE.txt file for details.

from __future__ import print_function
import csv
import os
import StringIO
import sys
import unicodedata

from collections import OrderedDict
from datetime import datetime

from fontaine.const import SUPPORT_LEVEL_FULL, SUPPORT_LEVEL_UNSUPPORTED
from fontaine.cmap import library
from fontaine.font import FontFactory
from fontaine.structures.dict2xml import dict2xml, dict2txt


def yesno(val):
    return 'yes' if val else 'no'


db = os.environ.get('UNAMES_DB') or os.path.join(os.path.dirname(__file__),
                                                 'charmaps', 'names.db',
                                                 'en.names-db')


def format(x):
    return u'U+%04x\x20\x20%s\x20\x20%s' % \
        (x, unichr(x), unicodedata.name(unichr(x), ''))


def unicodevalues_asstring(values):
    """ Return string with unicodenames (unless that is disabled) """
    if not os.environ.get('DISABLE_UNAMES'):
        return map(lambda x: '%s' % format(x).strip(), values)
    return map(lambda x: u'U+%04x %s' % (x, unichr(x)), sorted(values))


extract_firstline = lambda text: \
    (text or '').replace('\r', '\n').split('\n')[0]


class Director(object):

    def __init__(self, show_hilbert=None, charmaps=[], missing=False,
                 _library=None):
        self.show_hilbert = show_hilbert
        self.charmaps = filter(lambda x: x != '', charmaps)
        self.missingValues = missing
        strdate = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        self.output_directory = 'pyfontaine-%s' % strdate
        self.library = _library or library

    def represent_coverage_png(self, font):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        cmaps = filter(lambda x: hasattr(x, 'key'), self.library.charmaps)

        for cmap in cmaps:
            if self.charmaps:
                cn = getattr(cmap, 'common_name', False)
                nn = getattr(cmap, 'native_name', False)
                if cn and cn not in self.charmaps:
                    continue
                if nn and nn not in self.charmaps:
                    continue

            if cmap.key not in font._unicodeValues:
                continue

            filename = u'%s/%s-%s-hilbert' % (self.output_directory,
                                              font.common_name,
                                              cmap.common_name)

            txtFilename = filename + '.txt'
            fp = open(txtFilename, 'w+')

            glyphs = cmap.glyphs
            if callable(glyphs):
                glyphs = glyphs()
            for i, char in enumerate(sorted(glyphs)):
                flag = str(0)
                if char in font._unicodeValues:
                    flag = str(1)
                fp.write(str(i + 1) + ' ' + flag + '\n')

            fp.close()
            hilbertScript = ('simpleHilbertCurve'
                             ' --outFormat=png'
                             ' --level=3'
                             ' --out="%s" "%s"') % (filename, txtFilename)
            os.system(hilbertScript)

    def construct_tree(self, fonts):
        if self.show_hilbert:
            try:
                import matplotlib
            except ImportError:
                raise Exception('Install matplotlib to use --show-hilbert feature')
        tree = OrderedDict({'fonts': [], 'identical': True})

        # in process of generating fonts information tree collect for each
        # font character set. then compare them and if they are not identical
        # set to tree flag `identical` to `False`
        fonts_charactersets_names = []
        for font_filename in fonts:
            font = FontFactory.openfont(font_filename, charmaps=self.charmaps)

            F = OrderedDict()
            desc = OrderedDict()
            desc['commonName'] = font.common_name
            desc['subFamily'] = font.sub_family
            desc['style'] = font.style_flags
            desc['weight'] = font.weight
            desc['fixedWidth'] = yesno(font.is_fixed_width)
            desc['fixedSizes'] = yesno(font.has_fixed_sizes)
            desc['copyright'] = extract_firstline(font.copyright or '')
            desc['license'] = extract_firstline(font.license or '')
            desc['licenseUrl'] = font.license_url
            desc['version'] = font.version
            desc['vendor'] = extract_firstline(font.vendor or '')
            desc['vendorUrl'] = font.vendor_url
            desc['designer'] = font.designer
            desc['designerUrl'] = font.designer_url
            desc['glyphCount'] = font.glyph_num
            desc['characterCount'] = font.character_count

            font_charactersets_names = []
            for charmap, support_level, coverage, missing \
                    in font.get_orthographies(self.library):
                if support_level == SUPPORT_LEVEL_UNSUPPORTED:
                    continue
                if 'orthographies' not in desc:
                    desc['orthographies'] = []

                orth = OrderedDict({'orthography': OrderedDict()})
                orth['orthography']['commonName'] = charmap.common_name
                orth['orthography']['nativeName'] = charmap.native_name
                orth['orthography']['supportLevel'] = support_level

                if support_level != SUPPORT_LEVEL_FULL:
                    values = u'\n%s' % u'\n'.join(unicodevalues_asstring(missing))
                    orth['orthography']['percentCoverage'] = coverage
                    if self.missingValues:
                        orth['orthography']['missingValues'] = values

                desc['orthographies'].append(orth)
                font_charactersets_names.append(charmap.common_name)

            if fonts_charactersets_names:
                if (tree['identical'] and
                        fonts_charactersets_names != font_charactersets_names):
                    tree['identical'] = False

            if not fonts_charactersets_names:
                fonts_charactersets_names = font_charactersets_names

            if self.show_hilbert:
                self.represent_coverage_png(font)

            F['font'] = desc

            tree['fonts'].append(F)

        if len(tree['fonts']) == 1:
            tree.pop('identical')

        return tree


class Builder(object):

    @staticmethod
    def text_(tree):
        return dict2txt(tree, names=NAMES)

    @staticmethod
    def xml_(tree):
        return dict2xml({'report': tree})

    @staticmethod
    def json_(tree):
        items_length = 0
        pprint(tree, indent='', items_length=items_length)

    @staticmethod
    def csv_(fonts, _library=library):
        data = StringIO.StringIO()
        doc = csv.writer(data, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        headers = ['Family', 'Style']
        for subset in _library.charmaps:
            headers.append(subset.common_name.encode('ascii', 'ignore'))
        doc.writerow(headers)

        for filename in fonts:
            font = FontFactory.openfont(filename)
            row = [font.common_name.encode('ascii', 'ignore')]
            row += [font.sub_family.encode('ascii', 'ignore')]
            for subset in _library.charmaps:
                charmap, support_level, coverage, missing = font.get_othography_info(subset)
                row.append(str(coverage))
            doc.writerow(row)

        data.seek(0)
        return data.read()

    @staticmethod
    def wiki(fonts, _library=library):
        for font_filename in fonts:
            font = FontFactory.openfont(font_filename)
            print('=== %s ===' % font.common_name.encode('ascii', 'ignore'))
            print('{|')
            print('| colspan=3 |')
            for subset in _library.charmaps:
                charmap, supported, coverage, missing = font.get_othography_info(subset)
                if supported == SUPPORT_LEVEL_UNSUPPORTED:
                    continue

                glyphs = charmap.glyphs
                if callable(glyphs):
                    glyphs = glyphs()

                print('|-')
                print("| [[ %s ]] (%s/%s)  || style='text-align:right'" % (charmap.common_name, len(glyphs) - len(missing), len(glyphs)),
                      " | {{bartable|%s|%%|2||background:green}}" % coverage)
            print('|}')


NAMES = {
    'fonts': 'Fonts',
    'font': 'Font',
    'commonName': 'Common name',
    'nativeName': 'Native name',
    'subFamily': 'Sub family',
    'style': 'Style',
    'weight': 'Weight',
    'fixedWidth': 'Fixed width',
    'fixedSizes': 'Fixed sizes',
    'copyright': 'Copyright',
    'license': 'License',
    'licenseUrl': 'License url',
    'version': 'Version',
    'vendor': 'Vendor',
    'vendorUrl': 'Vendor url',
    'designer': 'Designer',
    'designerUrl': 'Designer url',
    'glyphCount': 'Glyph count',
    'characterCount': 'Character count',
    'orthographies': 'Orthographies',
    'orthography': 'Orthography',
    'supportLevel': 'Support level',
    'percentCoverage': 'Percent coverage',
    'missingValues': 'Missing values'
}


def pprint_dict(obj, indent, length):
    for i, key in enumerate(obj.keys()):
        comma = ', '
        if i + 1 == length:
            comma = ''
        if type(obj[key]) in [str, int, unicode]:
            value = unicode(obj[key]).replace('\n', ', ').strip(', ')
            value = value.replace('"', '\"').replace('\\', '\\\\')
            value = value.replace('\r', '')
            sys.stdout.write((u"%s  %r: \"%s\"%s" % (indent, key, value, comma)))
        else:
            sys.stdout.write((u"%s  %r:" % (indent, key)))
            pprint(obj[key], indent + '  ')


def pprint(obj, indent='', items_length=0):
    comma = ''
    if isinstance(obj, OrderedDict):
        length = len(obj.keys())
        if length == 1:
            pprint(obj[obj.keys()[0]], indent, items_length=items_length)
            return

        sys.stdout.write((u"%s{" % indent))
        pprint_dict(obj, indent, length)
        if items_length > 0:
            comma = ', '
        sys.stdout.write((u"%s}%s" % (indent, comma)))
    elif isinstance(obj, list):
        sys.stdout.write((u"%s[" % indent))
        length = len(obj)
        for i, o in enumerate(obj):
            length -= 1
            pprint(o, indent + '  ', items_length=length)
        sys.stdout.write((u"%s]%s" % (indent, comma)))
