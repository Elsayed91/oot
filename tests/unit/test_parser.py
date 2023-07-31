import os
import tempfile
import unittest
from pathlib import Path

from oot.m_exceptions import YAMLParseError
from oot.parser import parse_yaml_with_jinja


class TestParseYAMLWithJinja(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_yaml_no_templates(self):
        file_path = self.create_yaml_file("key: value")
        result = parse_yaml_with_jinja(file_path)
        self.assertEqual(result, {"key": "value"})

    def test_valid_yaml_with_templates_with_variables(self):
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_yaml_with_jinja(file_path, {"var": "value"})
        self.assertEqual(result, {"key": "value"})

    def test_invalid_yaml(self):
        file_path = self.create_yaml_file("key: value\nkey2")
        with self.assertRaises(YAMLParseError):
            parse_yaml_with_jinja(file_path)

    def test_invalid_jinja_syntax(self):
        file_path = self.create_yaml_file("key: {{ var ")
        with self.assertRaises(YAMLParseError):
            parse_yaml_with_jinja(file_path)

    def test_jinja_templates_invalid_variables(self):
        file_path = self.create_yaml_file("key: {{ 2var }}")
        with self.assertRaises(YAMLParseError):
            parse_yaml_with_jinja(file_path)

    def test_jinja_templates_variable_defined_in_both_environment_and_variables(self):
        os.environ["var"] = "value1"
        self.addCleanup(lambda: os.environ.pop("var", None))
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_yaml_with_jinja(file_path, {"var": "value2"})
        self.assertEqual(result, {"key": "value2"})

    def test_jinja_templates_variable_defined_with_default_value(self):
        file_path = self.create_yaml_file("key: {{ var|default('default') }}")
        result = parse_yaml_with_jinja(file_path)
        self.assertEqual(result, {"key": "default"})

    def create_yaml_file(self, content):
        file = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml")
        file.write(content)
        file.close()
        return file.name

    def test_empty_yaml(self):
        file_path = self.create_yaml_file("")
        result = parse_yaml_with_jinja(file_path)
        self.assertEqual(result, {})

    def test_jinja_templates_missing_variables(self):
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_yaml_with_jinja(file_path)
        self.assertEqual(result, {"key": None})

    def test_jinja_templates_variable_defined_in_environment(self):
        os.environ["var"] = "value"
        self.addCleanup(lambda: os.environ.pop("var", None))
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_yaml_with_jinja(file_path, {"var": "value"})
        self.assertEqual(result, {"key": "value"})

    def test_jinja_templates_variable_defined_with_default_value_and_environment_variable_defined(
        self,
    ):
        os.environ["var"] = "value"
        self.addCleanup(lambda: os.environ.pop("var", None))
        file_path = self.create_yaml_file("key: {{ var|default('default') }}")
        result = parse_yaml_with_jinja(file_path, {"var": "value"})
        self.assertEqual(result, {"key": "value"})

    def test_jinja_templates_variable_not_defined_in_environment(self):
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_yaml_with_jinja(file_path)
        self.assertEqual(result, {"key": None})

    def test_valid_yaml_with_templates_no_variables(self):
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_yaml_with_jinja(file_path)
        self.assertEqual(result, {"key": None})
