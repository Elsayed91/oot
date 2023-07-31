import logging

logger = logging.getLogger(__name__)


class TemplateNotFoundError(Exception):
    """
    Exception raised when a template is not found.

    Attributes:
        template_name: The name of the template that was not found.
        message: Explanation of the error.
    """

    def __init__(self, template_name: str) -> None:
        self.template_name = template_name
        self.message = f"Template not found: {self.template_name}"
        super().__init__(self.message)
        logger.error(self.message)


class YAMLParseError(Exception):
    """
    Exception raised for errors during the YAML parsing process.

    Attributes:
        message: Explanation of the error.
    """

    def __init__(
        self, message: str = "An error occurred during the YAML parsing process"
    ) -> None:
        self.message = message
        super().__init__(self.message)
        logger.error(self.message)


class ValidationError(Exception):
    """
    Exception raised for errors during the validation process.

    Attributes:
        message: Explanation of the error.
    """

    def __init__(
        self, message: str = "An error occurred during the validation process"
    ) -> None:
        self.message = message
        super().__init__(self.message)
        logger.error(self.message)
