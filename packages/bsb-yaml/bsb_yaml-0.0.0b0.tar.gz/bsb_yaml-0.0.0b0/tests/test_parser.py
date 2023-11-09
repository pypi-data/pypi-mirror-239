import unittest

from bsb import config


class TestYAML(unittest.TestCase):
    def test_yaml_parse(self):
        yaml = config.get_parser("yaml")
        tree, meta = yaml.parse("some_key: 5")
        self.assertEqual({"some_key": 5}, tree)

    def test_yaml_generate(self):
        yaml = config.get_parser("yaml")
        content = yaml.generate({"some_key": 5})
        self.assertEqual("some_key: 5\n", content)
