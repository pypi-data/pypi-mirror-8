# -*- coding: utf-8 -*-

__license__ = 'GPL 3'
__copyright__ = '2010, Hiroshi Miura <miurahr@linux.com>'
__docformat__ = 'restructuredtext en'
__all__ = ["Unihandecoder"]

'''
Decode unicode text to an ASCII representation of the text. 
Translate unicode characters to ASCII.

inspired from John's unidecode library.
Copyright(c) 2009, John Schember

Tranliterate the string from unicode characters to ASCII in Chinese and others.

'''
import unicodedata
from unihandecode.unidecoder import Unidecoder
from unihandecode.jadecoder import Jadecoder
from unihandecode.krdecoder import Krdecoder
from unihandecode.vndecoder import Vndecoder

class Unihandecoder(object):
    preferred_encoding = None
    decoder = None

    def __init__(self, lang="zh", encoding='utf-8'):
        self.preferred_encoding = encoding
        if lang == "ja":
            self.decoder = Jadecoder()
        elif lang == "kr":
            self.decoder = Krdecoder()
        elif lang == "vn":
            self.decoder = Vndecoder()
        else: #zh and others
            self.decoder = Unidecoder()

    def decode(self, text):
        try:
            unicode # python2
            if not isinstance(text, unicode):
                try:
                    text = unicode(text)
                except:
                    try:
                        text = text.decode(self.preferred_encoding)
                    except:
                        text = text.decode('utf-8', 'replace')
        except: # python3, str is unicode
            pass
        #at first unicode normalize it. (see Unicode standards)
        ntext = unicodedata.normalize('NFC',text)
        return self.decoder.decode(ntext)

def unidecode(text):
    '''
    backword compatibility to unidecode
    '''
    decoder = Unihandecoder()
    #at first unicode normalize it. (see Unicode standards)
    ntext = unicodedata.normalize('NFKC',text)
    return decoder.decode(ntext)
