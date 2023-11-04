#!/usr/bin/env python


"""
test varboxes modules
"""

import unittest
import time


from varboxes import VarBox


class TestVarBox(unittest.TestCase):

    """all test concerning VarBox. """

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_set(self):
        varbox1 = VarBox(app_name='test_varbox')
        timestamp = time.time()
        varbox1.test_variable = timestamp

        self.assertEqual(timestamp, varbox1.test_variable)

        varbox2 = VarBox(app_name='test_varbox')

        self.assertTrue(hasattr(varbox2, 'test_variable'))

        self.assertEqual(timestamp, varbox2.test_variable)


if __name__ == '__main__':
    pass
