import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from jinja2 import Environment

from .loaders import CustomYAMLTemplateLoader
from .m_exceptions import YAMLParseError

logger = logging.getLogger(__name__)


def parse_yaml_with_jinja(
    file_path: Union[str, Path], variables: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Parse a YAML file with Jinja templates.

    Args:
        file_path: The path to the YAML file.
        variables: Optional variables to be used in the templates.

    Returns:
        The parsed YAML data.

    Raises:
        YAMLParseError: If there's an error parsing the YAML data.
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    env = Environment(loader=CustomYAMLTemplateLoader(str(file_path.parent), variables))

    try:
        template = env.get_template(file_path.name)
        rendered_yaml = template.render(variables or {})
        parsed_yaml = yaml.safe_load(rendered_yaml)
        return parsed_yaml or {}
    except Exception as e:
        raise YAMLParseError("An error occurred while parsing the YAML file.") from e
