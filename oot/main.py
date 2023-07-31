import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .m_exceptions import ValidationError
from .parser import parse_yaml_with_jinja
from .schema_validator import SchemaValidator

logger = logging.getLogger(__name__)


def parse_file(
    file_path: Union[str, Path],
    context: Optional[Dict[str, str]] = None,
    validation_schema: Optional[str] = None,
) -> Union[str, Dict[str, Any]]:
    """
    Parse a file with options to parse Jinja templating, environment variables, or both.

    Args:
        file_path: The path to the file.
        context: Variables to be used in the template.
        validator: An optional SchemaValidator instance to validate the parsed data.

    Returns:
        The parsed data.

    Raises:
        ValidationError: If a validator is provided and the data does not conform to the schema.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    data = parse_yaml_with_jinja(str(file_path), context)

    if validation_schema is not None:
        try:
            validator = SchemaValidator(validation_schema)
            validator.validate(data)
        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise ValidationError(f"Validation error: {e}")

    return data
