# test_formats.py

import unittest
import os

from concepts.formats import Format, Cxt, Table, Csv, WikiTable

DIRECTORY = 'test-output'


class TestFormat(unittest.TestCase):

    def test_getitem(self):
        self.assertEqual(Format['cxt'], Cxt)
        self.assertEqual(Format['table'], Table)
        self.assertEqual(Format['csv'], Csv)
        self.assertEqual(Format['wikitable'], WikiTable)

    def test_getitem_invalid(self):
        with self.assertRaises(KeyError):
            Format['spam']


class LoadsDumps(object):

    def test_loads(self):
        try:
            objects, properties, bools = self.format.loads(self.result)
        except NotImplementedError:
            pass
        else:
            self.assertSequenceEqual(objects, self.objects)
            self.assertSequenceEqual(properties, self.properties)
            self.assertSequenceEqual(bools, self.bools)

    def test_dumps(self):
        result = self.format.dumps(self.objects, self.properties, self.bools)
        self.assertEqual(result, self.result)

    def test_dump_load(self, outdir=DIRECTORY):
        if not os.path.exists(outdir):
            os.mkdir(outdir)

        extension = getattr(self.format, 'extension', '.txt')
        filepath = os.path.join(outdir, self.__class__.__name__ + extension)
        self.format.dump(filepath,
            self.objects, self.properties, self.bools,
            self.encoding)

        try:
            objects, properties, bools = self.format.load(filepath, self.encoding)
        except NotImplementedError:
            pass
        else:
            self.assertSequenceEqual(objects, self.objects)
            self.assertSequenceEqual(properties, self.properties)
            self.assertSequenceEqual(bools, self.bools)


class Ascii(LoadsDumps):

    objects = ('Cheddar', 'Limburger')
    properties = ('in_stock', 'sold_out')
    bools = [(False, True), (False, True)]

    encoding = None


class Unicode(LoadsDumps):

    objects = (u'M\xf8\xf8se', 'Llama')
    properties = ('majestic', 'bites')
    bools = [(True, True), (False, False)]

    encoding = 'utf-8'


class TestCxtAscii(unittest.TestCase, Ascii):

    format = Cxt
    result = 'B\n\n2\n2\n\nCheddar\nLimburger\nin_stock\nsold_out\n.X\n.X\n'


class TextCxtUnicode(unittest.TestCase, Unicode):

    format = Cxt
    result = u'B\n\n2\n2\n\nM\xf8\xf8se\nLlama\nmajestic\nbites\nXX\n..\n'


class TestTableAscii(unittest.TestCase, Ascii):

    format = Table
    result = (
        '         |in_stock|sold_out|\n'
        'Cheddar  |        |X       |\n'
        'Limburger|        |X       |')


class TestTableUnicode(unittest.TestCase, Unicode):

    format = Table
    result = (
        u'     |majestic|bites|\n'
        u'M\xf8\xf8se|X       |X    |\n'
        u'Llama|        |     |')


class TestCsvAscii(unittest.TestCase, Ascii):

    format = Csv
    result = (
        ',in_stock,sold_out\r\n'
        'Cheddar,,X\r\n'
        'Limburger,,X\r\n')


class TestCsvUnicode(unittest.TestCase, Unicode):

    format = Csv
    result = (
        u',majestic,bites\r\n'
        u'M\xf8\xf8se,X,X\r\n'
        u'Llama,,\r\n')


class TestWikitableAscii(unittest.TestCase, Ascii):

    format = WikiTable
    result = (
        '{| class="featuresystem"\n'
        '!\n'
        '!in_stock!!sold_out\n'
        '|-\n'
        '!Cheddar\n'
        '|        ||X       \n'
        '|-\n'
        '!Limburger\n'
        '|        ||X       \n'
        '|}')


class TestWikitableUnicode(unittest.TestCase, Unicode):

    format = WikiTable
    result = (
        u'{| class="featuresystem"\n'
        u'!\n'
        u'!majestic!!bites\n'
        u'|-\n'
        u'!M\xf8\xf8se\n|X       ||X    \n'
        u'|-\n'
        u'!Llama\n'
        u'|        ||     \n'
        '|}')
