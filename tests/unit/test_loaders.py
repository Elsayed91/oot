import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from jinja2.exceptions import TemplateNotFound

from oot.loaders import CustomYAMLTemplateLoader
from oot.m_exceptions import TemplateNotFoundError


class TestCustomYAMLTemplateLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.template_dir = Path(self.test_dir.name)
        self.variables = {"var1": "value1", "var2": "value2"}

    def tearDown(self):
        self.test_dir.cleanup()

    @patch("pathlib.Path.is_dir")
    def test_load_valid_dir(self, mock_is_dir):
        mock_is_dir.return_value = True
        loader = CustomYAMLTemplateLoader(str(self.template_dir))
        self.assertEqual(loader.path, self.template_dir)

    @patch("pathlib.Path.is_dir")
    def test_load_valid_dir_with_variables(self, mock_is_dir):
        mock_is_dir.return_value = True
        loader = CustomYAMLTemplateLoader(str(self.template_dir), self.variables)
        self.assertEqual(loader.path, self.template_dir)
        self.assertEqual(loader.variables, self.variables)

    @patch("pathlib.Path.is_dir")
    def test_load_invalid_dir(self, mock_is_dir):
        mock_is_dir.return_value = False
        with self.assertRaises(ValueError):
            CustomYAMLTemplateLoader(str(self.template_dir))

    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.iterdir")
    def test_load_dir_no_templates(self, mock_iterdir, mock_is_dir):
        mock_is_dir.return_value = True
        mock_iterdir.return_value = iter([])  # Empty directory
        with self.assertRaises(TemplateNotFoundError):
            loader = CustomYAMLTemplateLoader(str(self.template_dir))
            loader.get_source(None, "any_template.yaml")

    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.iterdir")
    def test_load_dir_non_yaml_templates(self, mock_iterdir, mock_is_dir):
        mock_is_dir.return_value = True
        mock_iterdir.return_value = iter([Path("template.txt")])  # Non-YAML template
        with self.assertRaises(TemplateNotFoundError):
            loader = CustomYAMLTemplateLoader(str(self.template_dir))
            loader.get_source(None, "any_template.yaml")

    @patch("pathlib.Path.exists")
    def test_get_source_non_existing_template(self, mock_exists):
        mock_exists.return_value = False
        loader = CustomYAMLTemplateLoader(str(self.template_dir), self.variables)
        with self.assertRaises(TemplateNotFoundError):
            loader.get_source(None, "non_existing_template.yaml")

    def test_preprocess_yaml_default_value(self):
        loader = CustomYAMLTemplateLoader(str(self.template_dir))
        os.environ.pop("var1", None)
        yaml_content = "${var1:default}"
        preprocessed = loader.preprocess_yaml(yaml_content)
        self.assertEqual(preprocessed, "default")

    def test_get_source_existing_template(self):
        loader = CustomYAMLTemplateLoader(str(self.template_dir), self.variables)
        template_file = self.template_dir / "existing_template.yaml"
        template_file.write_text("test content")
        source, filename, uptodate = loader.get_source(None, "existing_template.yaml")
        self.assertIsInstance(source, str)
        self.assertEqual(filename, str(template_file))
        self.assertFalse(uptodate())

    def test_preprocess_valid_yaml(self):
        loader = CustomYAMLTemplateLoader(str(self.template_dir), self.variables)
        os.environ["var1"] = "value1"
        os.environ["var2"] = "value2"
        yaml_content = "${var1}\n${var2}"
        preprocessed = loader.preprocess_yaml(yaml_content)
        self.assertEqual(preprocessed, "value1\nvalue2")

    def test_preprocess_invalid_yaml(self):
        loader = CustomYAMLTemplateLoader(str(self.template_dir))
        invalid_yaml_content = "${:}"
        with self.assertRaises(ValueError):
            loader.preprocess_yaml(invalid_yaml_content)

    def test_preprocess_yaml_missing_env_var(self):
        loader = CustomYAMLTemplateLoader(str(self.template_dir))
        os.environ.pop("var1", None)
        yaml_content = "${var1}"
        preprocessed = loader.preprocess_yaml(yaml_content)
        self.assertEqual(preprocessed, "")
