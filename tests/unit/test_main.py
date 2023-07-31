import os
import tempfile
import unittest
from unittest.mock import patch

from oot.m_exceptions import ValidationError, YAMLParseError
from oot.main import parse_file


class TestParseFile(unittest.TestCase):
    def create_yaml_file(self, content):
        file = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml")
        file.write(content)
        file.close()
        return file.name

    def test_parsing_yaml_with_jinja_no_validation_schema(self):
        file_path = self.create_yaml_file("key: {{ var }}")
        result = parse_file(file_path, context={"var": "value"})
        self.assertEqual(result, {"key": "value"})

    def test_parsing_yaml_with_jinja_and_validation_schema(self):
        file_path = self.create_yaml_file("key: {{ var }}")
        schema_path = self.create_yaml_file(
            '{"type": "object", "properties": {"key": {"type": "string"}}}'
        )
        result = parse_file(
            file_path, context={"var": "value"}, validation_schema=schema_path
        )
        self.assertEqual(result, {"key": "value"})

    def test_parsing_yaml_with_env_vars_no_validation_schema(self):
        file_path = self.create_yaml_file("key: ${VAR}")
        os.environ["VAR"] = "value"
        result = parse_file(file_path)
        self.assertEqual(result, {"key": "value"})

    def test_parsing_yaml_with_env_vars_and_validation_schema(self):
        file_path = self.create_yaml_file("key: ${VAR}")
        schema_path = self.create_yaml_file(
            '{"type": "object", "properties": {"key": {"type": "string"}}}'
        )
        os.environ["VAR"] = "value"
        result = parse_file(file_path, validation_schema=schema_path)
        self.assertEqual(result, {"key": "value"})

    def test_parsing_yaml_with_jinja_and_env_vars_no_validation_schema(self):
        file_path = self.create_yaml_file("key: {{ var }}-${VAR}")
        os.environ["VAR"] = "value"
        result = parse_file(file_path, context={"var": "value"})
        self.assertEqual(result, {"key": "value-value"})

    def test_parsing_yaml_with_jinja_and_env_vars_and_validation_schema(self):
        file_path = self.create_yaml_file("key: {{ var }}-${VAR}")
        schema_path = self.create_yaml_file(
            '{"type": "object", "properties": {"key": {"type": "string"}}}'
        )
        os.environ["VAR"] = "value"
        result = parse_file(
            file_path, context={"var": "value"}, validation_schema=schema_path
        )
        self.assertEqual(result, {"key": "value-value"})

    def test_parsing_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            parse_file("non_existent_file.yaml")

    def test_parsing_invalid_yaml(self):
        file_path = self.create_yaml_file("{invalid yaml")
        with self.assertRaises(Exception):
            parse_file(file_path)

    def test_parsing_invalid_jinja(self):
        file_path = self.create_yaml_file("key: {{ var ")
        with self.assertRaises(Exception):
            parse_file(file_path)

    def test_parsing_invalid_env_var(self):
        file_path = self.create_yaml_file("key: ${VAR:")
        os.environ.pop("VAR", None)
        with self.assertRaises(YAMLParseError):
            parse_file(file_path)

    def test_parsing_invalid_validation_schema(self):
        file_path = self.create_yaml_file("key: value")
        schema_path = self.create_yaml_file("{invalid json")
        with self.assertRaises(Exception):
            parse_file(file_path, validation_schema=schema_path)

    def test_validation_error(self):
        file_path = self.create_yaml_file("key: value")
        schema_path = self.create_yaml_file(
            '{"type": "object", "properties": {"key": {"type": "integer"}}}'
        )
        with self.assertRaises(ValidationError):
            parse_file(file_path, validation_schema=schema_path)

    def test_return_empty_dict_if_yaml_is_none(self):
        file_path = self.create_yaml_file("")
        result = parse_file(file_path)
        self.assertEqual(result, {})

    @patch("oot.main.logger")
    def test_log_error_if_file_not_found(self, mock_logger):
        with self.assertRaises(FileNotFoundError):
            parse_file("non_existent_file.yaml")
        self.assertTrue(mock_logger.error.called)

    @patch("oot.main.logger")
    def test_log_error_if_validation_error(self, mock_logger):
        file_path = self.create_yaml_file("key: value")
        schema_path = self.create_yaml_file(
            '{"type": "object", "properties": {"key": {"type": "integer"}}}'
        )
        with self.assertRaises(ValidationError):
            parse_file(file_path, validation_schema=schema_path)
        self.assertTrue(mock_logger.error.called)

    def test_raise_json_decode_error_if_invalid_json_in_schema(self):
        file_path = self.create_yaml_file("key: value")
        schema_path = self.create_yaml_file("{invalid json")
        with self.assertRaises(Exception):
            parse_file(file_path, validation_schema=schema_path)
