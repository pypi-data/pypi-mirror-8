from __future__ import unicode_literals

import unittest

from mopidy_yamaha import Extension


class ExtensionTest(unittest.TestCase):

    def test_get_default_config(self):
        ext = Extension()

        config = ext.get_default_config()

        self.assertIn('[yamaha]', config)
        self.assertIn('enabled = true', config)

    def test_get_config_schema(self):
        ext = Extension()

        schema = ext.get_config_schema()

        self.assertIn('enabled', schema)
        self.assertIn('host', schema)
        self.assertIn('source', schema)
        self.assertIn('party_mode', schema)
