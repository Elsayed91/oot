import logging
import os
import re
from pathlib import Path
from typing import Callable, Optional, Tuple

from jinja2 import BaseLoader

from .m_exceptions import TemplateNotFoundError

logger = logging.getLogger(__name__)


class CustomYAMLTemplateLoader(BaseLoader):
    """
    Handles preprocessing of YAML templates.
    """

    ENV_VAR_PATTERN = re.compile(r"\$\{([^:}]+)(?::([^}]+))?\}")

    def __init__(self, template_path: str, variables: Optional[dict] = None) -> None:
        """
        Initialize a CustomYAMLTemplateLoader instance.

        Args:
            template_path: The path to the template files.
            variables: Optional variables to be used in the templates.
        """
        self.path = Path(template_path)
        if not self.path.is_dir():
            raise ValueError(f"Invalid directory path: {self.path}")

        self.variables = variables if variables else {}

    def get_source(self, env, template: str) -> Tuple[str, str, Callable[[], bool]]:
        """
        Get the source code of a template file.

        Args:
            env: The Jinja2 environment.
            template: The name of the template file.

        Returns:
            The source code of the template file and a function that
            returns False indicating the source code hasn't changed.

        Raises:
            TemplateNotFoundError: If the template file cannot be found.
        """
        filename = self.path / template
        if not filename.exists():
            raise TemplateNotFoundError(template)

        try:
            with open(filename, "r") as file:
                yaml_content = file.read()
        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
            raise

        template_content = self.preprocess_yaml(yaml_content)

        return template_content, str(filename), lambda: False

    def preprocess_yaml(self, yaml_content: str) -> str:
        """
        Preprocess a YAML template.

        Args:
            yaml_content: The content of the YAML template.

        Returns:
            The preprocessed YAML content.

        Raises:
            ValueError: If the YAML content is not valid.
        """
        INVALID_ENV_VAR_PATTERN = re.compile(r"\$\{:\}")

        if INVALID_ENV_VAR_PATTERN.search(yaml_content):
            raise ValueError("Invalid environment variable in YAML content.")

        def replace_env_var(match):
            var, default = match.groups()
            return os.environ.get(var.strip(), default if default else "")

        return self.ENV_VAR_PATTERN.sub(replace_env_var, yaml_content)
