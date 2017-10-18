import unittest
from san_config import *


class TestSanConfig(unittest.TestCase):
    def setUp(self):
        with open('cfgshow.txt', 'r') as fd:
            self.config = fd.read()

    def test_extract_defined_config(self):
        """It has to extract the defined configuration out of
        the given a SAN config.
        """
        expected = '''Defined configuration:
 cfg:   san01   cs5k1_fc1_a_to_cdp01_fca_100_i_zone;
                cs5k1_fc1_a_to_cdp01_fca_102_i_zone;
                cs5k1_fc1_a_to_cdp02_fca_100_i_zone;
                cs5k1_fc1_a_to_cdp02_fca_102_i_zone;
                cs5k1_fc2_a_to_cdp01_fca_100_i_zone;
                cs5k1_fc2_a_to_cdp01_fca_102_i_zone;
                cs5k1_fc2_a_to_cdp02_fca_100_i_zone;
                cs5k1_fc2_a_to_cdp02_fca_102_i_zone;
 zone:  cs5k1_fc1_a_to_cdp01_fca_100_i_zone
                cs5k1_fc1_a; cdp01_fca_100_i
 zone:  cs5k1_fc1_a_to_cdp01_fca_102_i_zone
                cs5k1_fc1_a; cdp01_fca_102_i
 zone:  cs5k1_fc1_a_to_cdp02_fca_100_i_zone
                cs5k1_fc1_a; cdp02_fca_100_i
 zone:  cs5k1_fc1_a_to_cdp02_fca_102_i_zone
                cs5k1_fc1_a; cdp02_fca_102_i
 zone:  cs5k1_fc2_a_to_cdp01_fca_100_i_zone
                cs5k1_fc2_a; cdp01_fca_100_i
 zone:  cs5k1_fc2_a_to_cdp01_fca_102_i_zone
                cs5k1_fc2_a; cdp01_fca_102_i
 zone:  cs5k1_fc2_a_to_cdp02_fca_100_i_zone
                cs5k1_fc2_a; cdp02_fca_100_i
 zone:  cs5k1_fc2_a_to_cdp02_fca_102_i_zone
                cs5k1_fc2_a; cdp02_fca_102_i
 alias: cdp01_fca_100_i
                21:00:00:24:ff:3a:3d:3a
 alias: cdp01_fca_102_i
                21:00:00:24:ff:33:ea:5a
 alias: cdp02_fca_100_i
                21:00:00:24:ff:44:51:4e
 alias: cdp02_fca_102_i
                21:00:00:24:ff:3e:3e:da
 alias: cs5k1_fc1_a
                56:c9:ce:90:70:ae:75:01
 alias: cs5k1_fc2_a
                56:c9:ce:90:70:ae:75:02
'''

        defined_config = extract_defined_config(self.config)

        self.assertEqual(expected, defined_config)

    def test_extract_effective_config(self):
        """It has to extract the effective configuration out of
        the given SAN config.
        """

        expected = '''Effective configuration:
 cfg:   san01
 zone:  cs5k1_fc1_a_to_cdp01_fca_100_i_zone
                56:c9:ce:90:70:ae:75:01
                21:00:00:24:ff:3a:3d:3a
 zone:  cs5k1_fc1_a_to_cdp01_fca_102_i_zone
                56:c9:ce:90:70:ae:75:01
                21:00:00:24:ff:33:ea:5a
 zone:  cs5k1_fc1_a_to_cdp02_fca_100_i_zone
                56:c9:ce:90:70:ae:75:01
                21:00:00:24:ff:44:51:4e
 zone:  cs5k1_fc1_a_to_cdp02_fca_102_i_zone
                56:c9:ce:90:70:ae:75:01
                21:00:00:24:ff:3e:3e:da
 zone:  cs5k1_fc2_a_to_cdp01_fca_100_i_zone
                56:c9:ce:90:70:ae:75:02
                21:00:00:24:ff:3a:3d:3a
 zone:  cs5k1_fc2_a_to_cdp01_fca_102_i_zone
                56:c9:ce:90:70:ae:75:02
                21:00:00:24:ff:33:ea:5a
 zone:  cs5k1_fc2_a_to_cdp02_fca_100_i_zone
                56:c9:ce:90:70:ae:75:02
                21:00:00:24:ff:44:51:4e
 zone:  cs5k1_fc2_a_to_cdp02_fca_102_i_zone
                56:c9:ce:90:70:ae:75:02
                21:00:00:24:ff:3e:3e:da
'''

        effective_config = extract_effective_config(self.config)

        self.assertEqual(expected, effective_config)

    def test_alias_regex_match_when_1_alias_1_wwpn(self):
        """It verifies that the alias regex again't the given content."""

        alias = ''' alias: cdp01_fca_100_i
                21:00:00:24:ff:3a:3d:3a
'''
        expected = [{'cdp01_fca_100_i': ['21:00:00:24:ff:3a:3d:3a']}]
        aliases = get_alias(alias)

        self.assertListEqual(expected, aliases)

    def test_alias_regex_match_when_1_alias_2_wwpns(self):
        """It verifies that the alias regex again't the given content."""

        alias = ''' alias: cdp01_fca_100_i
                21:00:00:24:ff:3a:3d:3a
                AA:AA:AA:AA:AA:AA:AA:AA
'''
        expected = [{'cdp01_fca_100_i': [
            '21:00:00:24:ff:3a:3d:3a',
            'AA:AA:AA:AA:AA:AA:AA:AA']}]
        aliases = get_alias(alias)

        self.assertListEqual(expected, aliases)

    def test_alias_regex_match_when_1_alias_3_wwpns(self):
        """It verifies that the alias regex again't the given content."""

        alias = ''' alias: cdp01_fca_100_i
                21:00:00:24:ff:3a:3d:3a
                AA:AA:AA:AA:AA:AA:AA:AA
                BB:BB:BB:BB:BB:BB:BB:BB
'''
        expected = [{'cdp01_fca_100_i': [
            '21:00:00:24:ff:3a:3d:3a',
            'AA:AA:AA:AA:AA:AA:AA:AA',
            'BB:BB:BB:BB:BB:BB:BB:BB',
            ]}]
        aliases = get_alias(alias)

        self.assertListEqual(expected, aliases)