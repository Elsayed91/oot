import json
import unittest
from json import JSONDecodeError
from tempfile import TemporaryDirectory

from jsonschema import ValidationError as JsonSchemaValidationError

from oot.m_exceptions import ValidationError
from oot.schema_validator import SchemaValidator


class TestSchemaValidator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.valid_schema_file = self.temp_dir.name + "/valid_schema.json"
        self.invalid_schema_file = self.temp_dir.name + "/invalid_schema.json"
        with open(self.valid_schema_file, "w") as f:
            json.dump(
                {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
                f,
            )
        with open(self.invalid_schema_file, "w") as f:
            f.write("invalid json")

    def test_load_valid_schema_file(self):
        SchemaValidator(self.valid_schema_file)

    def test_load_invalid_schema_file(self):
        with self.assertRaises(json.JSONDecodeError):
            SchemaValidator(self.invalid_schema_file)

    def test_validate_conforming_data(self):
        validator = SchemaValidator(self.valid_schema_file)
        validator.validate({"name": "test"})

    def test_validate_non_conforming_data(self):
        validator = SchemaValidator(self.valid_schema_file)
        with self.assertRaises(ValidationError):
            validator.validate({"name": 123})

    def test_validate_empty_data(self):
        validator = SchemaValidator(self.valid_schema_file)
        with self.assertRaises(ValidationError):
            validator.validate({})

    def test_validate_data_missing_properties(self):
        validator = SchemaValidator(self.valid_schema_file)
        with self.assertRaises(ValidationError):
            validator.validate({})

    def test_validate_data_additional_properties(self):
        validator = SchemaValidator(self.valid_schema_file)
        # This will pass as our schema does not disallow additional properties
        validator.validate({"name": "test", "extra": "property"})

    def test_validate_data_nested_properties(self):
        nested_schema_file = self.temp_dir.name + "/nested_schema.json"
        with open(nested_schema_file, "w") as f:
            json.dump(
                {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "object",
                            "properties": {
                                "first": {"type": "string"},
                                "last": {"type": "string"},
                            },
                            "required": ["first", "last"],
                        }
                    },
                    "required": ["name"],
                },
                f,
            )
        validator = SchemaValidator(nested_schema_file)
        with self.assertRaises(ValidationError):
            validator.validate({"name": {"first": "test"}})
        validator.validate({"name": {"first": "test", "last": "user"}})

    def test_validate_data_different_data_types(self):
        validator = SchemaValidator(self.valid_schema_file)
        with self.assertRaises(ValidationError):
            validator.validate({"name": 123})
        validator.validate({"name": "test"})

    def test_validate_data_with_arrays(self):
        array_schema_file = self.temp_dir.name + "/array_schema.json"
        with open(array_schema_file, "w") as f:
            json.dump(
                {
                    "type": "object",
                    "properties": {
                        "names": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["names"],
                },
                f,
            )
        validator = SchemaValidator(array_schema_file)
        with self.assertRaises(ValidationError):
            validator.validate({"names": ["test", 123]})
        validator.validate({"names": ["test", "user"]})

    def tearDown(self):
        self.temp_dir.cleanup()
