# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import sys
from nose.tools import *

sys.path.insert(0, os.path.abspath('..'))

try:
    from translator import translator
except ImportError:
    from translate import translator


class TestTranslator(unittest.TestCase):

    def typeassert(self):
        instance = translator('en', 'en', str())
        self.assertIsInstance(instance, dict)
        self.assertIsInstance(instance['sentences'], list)
        self.assertIsInstance(instance['sentences'][0], dict)
        self.assertIsInstance(instance['sentences'][0]['trans'], str)

    def test_love(self):
        love = translator('en', 'zh-TW', 'I love you')['sentences'][0]['trans']
        self.assertEqual(love, u'我愛你')


if __name__ == '__main__':
    unittest.main()
