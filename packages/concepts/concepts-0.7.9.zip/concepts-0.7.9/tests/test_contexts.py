# test_contexts.py

import unittest

from concepts.contexts import Context


class TestContextInit(unittest.TestCase):

    def test_duplicate_object(self):
        with self.assertRaises(ValueError):
            Context(('spam', 'spam'), ('ham', 'eggs'),
                [(True, False), (False, True)])

    def test_duplicate_property(self):
        with self.assertRaises(ValueError):
            Context(('spam', 'eggs'), ('ham', 'ham'),
                [(True, False), (False, True)])

    def test_object_property_overlap(self):
        with self.assertRaises(ValueError):
            Context(('spam', 'eggs'), ('eggs', 'ham'),
                [(True, False), (False, True)])

    def test_empty_relation(self):
        with self.assertRaises(ValueError):
            Context((), ('spam',), [(False,)])
        with self.assertRaises(ValueError):
            Context(('spam',), (), [(False,)])

    def test_invalid_bools(self):
        with self.assertRaises(ValueError):
            Context(('spam', 'eggs'), ('camelot', 'launcelot'),
                [(True, False)])
        with self.assertRaises(ValueError):
            Context(('spam', 'eggs'), ('camelot', 'launcelot'),
                [(True, False, False), (False, True)])

    def test_init(self):
        c = Context(('spam', 'eggs'), ('camelot', 'launcelot'),
            [(True, False), (False, True)])
        self.assertEqual(c.objects, ('spam', 'eggs'))
        self.assertEqual(c.properties, ('camelot', 'launcelot'))
        self.assertEqual(c.bools, [(True, False), (False, True)])


class TestContext(unittest.TestCase):

    source = '''
       |+1|-1|+2|-2|+3|-3|+sg|+pl|-sg|-pl|
    1sg| X|  |  | X|  | X|  X|   |   |  X|
    1pl| X|  |  | X|  | X|   |  X|  X|   |
    2sg|  | X| X|  |  | X|  X|   |   |  X|
    2pl|  | X| X|  |  | X|   |  X|  X|   |
    3sg|  | X|  | X| X|  |  X|   |   |  X|
    3pl|  | X|  | X| X|  |   |  X|  X|   |
    '''

    @classmethod
    def setUpClass(cls, source=None):
        if source is None:
            source = cls.source
        cls.context = Context.fromstring(source)

    @classmethod
    def tearDownClass(cls):
        del cls.context

    def test_eq(self):
        self.assertTrue(self.context ==
            Context(self.context.objects, self.context.properties,
                self.context.bools))

    def test_eq_undefined(self):
        self.assertFalse(self.context == object())

    def test_ne(self):
        self.assertTrue(self.context !=
            Context(('spam', 'eggs'), ('camelot', 'launcelot'),
                [(True, False), (False, True)]))

    def test_minimize_infimum(self):
        self.assertEqual(list(self.context._minimize((), self.context.properties)),
            [self.context.properties])

    def test_raw(self):
        Extent, Intent = self.context._Extent, self.context._Intent
        self.assertEqual(self.context.intension(['1sg', '1pl'], raw=True),
            Intent('1001010000'))
        self.assertEqual(self.context.extension(['+1', '+sg'], raw=True),
            Extent('100000'))
        self.assertEqual(self.context.neighbors(['1sg'], raw=True),
            [(Extent('110000'), Intent('1001010000')),
             (Extent('101000'), Intent('0000011001')),
             (Extent('100010'), Intent('0001001001'))])

    def test_unicode(self):
        assert all(ord(c) < 128 for c in str(self.context))
        self.assertEqual(u'%s' % self.context, '%s' % self.context)
