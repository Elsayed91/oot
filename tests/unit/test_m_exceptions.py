import unittest
from unittest.mock import patch

from oot.m_exceptions import (TemplateNotFoundError, ValidationError,
                              YAMLParseError)


class TestMExceptions(unittest.TestCase):
    @patch("oot.m_exceptions.logger")
    def test_template_not_found_error(self, mock_logger):
        with self.assertRaises(TemplateNotFoundError) as cm:
            raise TemplateNotFoundError("template.yaml")

        self.assertEqual(str(cm.exception), "Template not found: template.yaml")
        self.assertTrue(mock_logger.error.called)

    @patch("oot.m_exceptions.logger")
    def test_yaml_parse_error(self, mock_logger):
        with self.assertRaises(YAMLParseError) as cm:
            raise YAMLParseError("Error during YAML parsing")

        self.assertEqual(str(cm.exception), "Error during YAML parsing")
        self.assertTrue(mock_logger.error.called)

    @patch("oot.m_exceptions.logger")
    def test_validation_error(self, mock_logger):
        with self.assertRaises(ValidationError) as cm:
            raise ValidationError("Error during validation")

        self.assertEqual(str(cm.exception), "Error during validation")
        self.assertTrue(mock_logger.error.called)
