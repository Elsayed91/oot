import os
import tempfile
import unittest

from oot.main import parse_file


class TestIntegration(unittest.TestCase):
    def create_yaml_file(self, content):
        file = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".yaml")
        file.write(content)
        file.close()
        return file.name

    def test_integration(self):
        os.environ["VALID"] = "valid_value"
        template = """
            Project: ${VALID:default_value}
            Bucket: {{ BUCKET }}
            ExpectationSuiteName: ${VALID:default_value}
            REASON: {{TEST.UNIT.DEPENDENCY}}
        """
        file_path = self.create_yaml_file(template)
        context = {
            "BUCKET": "bucket_value",
            "TEST": {"UNIT": {"DEPENDENCY": "dependency_value"}},
        }
        schema_path = self.create_yaml_file(
            """
            {
                "type": "object",
                "properties": {
                    "Project": {"type": "string"},
                    "Bucket": {"type": "string"},
                    "ExpectationSuiteName": {"type": "string"},
                    "REASON": {"type": "string"}
                }
            }
        """
        )
        expected_result = {
            "Project": "valid_value",
            "Bucket": "bucket_value",
            "ExpectationSuiteName": "valid_value",
            "REASON": "dependency_value",
        }
        result = parse_file(file_path, context=context, validation_schema=schema_path)
        self.assertEqual(result, expected_result)
