import re

from fontaine.ext.base import BaseExt
from fontaine.ext.update import get_from_cache

UNIDATA_URL = 'http://www.unicode.org/Public/UNIDATA/Blocks.txt'


class Extension(BaseExt):

    extension_name = 'uniblocks'

    @staticmethod
    def __getcharmaps__():
        content = open(get_from_cache('Blocks.txt', UNIDATA_URL), 'r').read()

        regex = re.compile('^([\da-f]+)..([\da-f]+);\s*(.*)$', re.I | re.U)
        for line in content.split('\n'):
            m = regex.match(line.strip())
            # 100000..10FFFF; Supplementary Private Use Area-B
            if not m:
                continue

            glyphlist = '0x%s-0x%s' % (m.group(1), m.group(2))
            unicodes = Extension.convert_to_list_of_unicodes(glyphlist)
            yield type('Charmap', (object,),
                       dict(glyphs=unicodes,
                            common_name=u'Unicode Block %s' % m.group(3),
                            native_name=''))
