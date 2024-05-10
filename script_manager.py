# Standard
import json
from enum import Enum

# Project
import config as cf

class Templates(Enum):
    """The Templates class defines template paths"""

    # Points to the script_template.txt file under the template directory
    NEW = cf.TEMPLATE_PATH / "script_template.txt"
    # EXPAND: Points to the expand_script_template.txt file under the template directory
    EXPAND = cf.TEMPLATE_PATH / "expand_script_template.txt"


class InvalidArgumentException(Exception):
    """Custom exception class for invalid arguments.

    Args:
        Exception (_type_): Base exception class
    """

    def __init__(self, message):
        self.message = message


async def scriptize_prompt(prompt: str, template: Templates) -> str:
    """Generates a scripted prompt using the given template.

    Args:
        prompt (str): The input prompt text.
        template (Templates): The template to generate the prompt.

    Returns:
        str: The scriptized prompt.
    """
    match template:
        case Templates.NEW:
            template = await __get_script_template(template=Templates.NEW)
            scriptized_prompt = template.format(theme=prompt)
        case Templates.EXPAND:
            template = await __get_script_template(template=Templates.EXPAND)
            scriptized_prompt = template.format(current_data=prompt)

    return scriptized_prompt


async def __get_script_template(template: Templates) -> str:
    """Retrieves the script template contents.

    Returns:
        str: The contents of the script template.
    """
    with open(file=template.value, mode="r", encoding="utf-8") as template:
        return template.read()
