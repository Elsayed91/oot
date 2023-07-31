import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Callable, Dict, cast

import fastjsonschema

from .m_exceptions import ValidationError

logger = logging.getLogger(__name__)


class SchemaValidator:
    """
    Handles validation of data against a JSON schema.
    """

    def __init__(self, schema_path: str) -> None:
        """
        Initialize a SchemaValidator instance.

        Args:
            schema_path: The path to the JSON schema file. (str)
        """
        self._schema_path = Path(schema_path)
        if not self._schema_path.is_file():
            raise FileNotFoundError(f"Schema file not found: {self._schema_path}")
        self._schema = self._load_schema()
        self._validator = cast(
            Callable[[Dict[str, Any]], None], fastjsonschema.compile(self._schema)
        )

    def _load_schema(self) -> Dict[str, Any]:
        """
        Load and cache the JSON schema from the file.

        Returns:
            The loaded JSON schema. (Dict[str, Any])

        Raises:
            JSONDecodeError: If the schema file does not contain valid JSON.
        """
        try:
            with open(self._schema_path, "r") as f:
                return json.load(f)
        except JSONDecodeError as e:
            raise JSONDecodeError(
                "Invalid JSON format in schema file.", e.doc, e.pos
            ) from e

    def validate(self, data: Dict[str, Any]) -> None:
        """
        Validate data against the loaded JSON schema.

        Args:
            data: The data to be validated. (Dict[str, Any])

        Raises:
            ValidationError: If the data doesn't conform to the schema.
        """
        try:
            self._validator(data)
        except fastjsonschema.JsonSchemaException as e:
            raise ValidationError(f"Validation error: {str(e)}") from e
