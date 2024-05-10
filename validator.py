# Third-party
from jsonschema import validate

# Standard
import json
from enum import Enum

# Project
import config as cf


class Roles(Enum):
    WIZARD = 'WIZARD'
    MAIN = 'MAIN'
    NECROMANCER = 'NECROMANCER'
    KNIGHT = 'KNIGHT'


class Methods(Enum):
    COME = 'come_to'
    DIALOGUE = 'begin_dialogue_to'


class JSONValidator:
    """
    A class to validate and modify JSON responses according to given rules.
    """

    def __init__(self, json_data: str | dict):
        """
        Initializes the JSONValidator with JSON data.
        
        :param json_data: The JSON data to validate and modify.
        """
        if isinstance(json_data, str):
            self.json_data = json.loads(json_data)
        else:
            self.json_data = json_data

    def validate_and_modify_json(self) -> dict | str:
        """
        Validates and modifies the JSON response.
        
        Returns modified JSON if adjustments were needed or the initial JSON if it was already valid.
        """
        try:
            self._find_and_make_roles_upper()
            print('structure', self._validate_structure())
            print('actions', self._validate_actions())
            print('dialogues', self._validate_dialogues())
            if self._validate_structure() and self._validate_actions() and self._validate_dialogues():
                # If all validations pass without modifying, return the original JSON.
                return self.json_data
            else:
                # If modifications were made, return the modified JSON.
                return self.json_data
        except Exception as e:
            return f"Error in validation: {str(e)}"
        
    def _find_and_make_roles_upper(self):
        """
        Finds all roles in the actions list and makes them uppercase.
        
        Modifies the JSON data in place.
        """
        for script_item in self.json_data.get("script", []):
            actions = script_item.get("actions", [])
            for i, action in enumerate(actions):
                method, role = action.replace('(', ' ').replace(')', '').split()
                if role.lower() in [role.value.lower() for role in Roles]:
                    actions[i] = f"{method}({role.upper()})"

    def _validate_structure(self) -> bool:
        """
        Validates the structure of a given JSON data against a predefined schema.
        
        Args:
            data (dict): The JSON data to validate.
        
        Returns:
            bool: True if the data matches the schema, False otherwise.
        """
        
        # Define the schema for validation
        with open(cf.BASE_PATH / '_schema.json', 'r') as f:
            schema = json.load(f)
        
            # Validate the data against the schema
        validate(instance=self.json_data, schema=schema)
        return True
        

    def _validate_actions(self) -> bool:
        """
        Validates the actions according to the rule that 'begin_dialogue_to' must come after other functions.
        
        Raises an exception if the rule is violated.
        """
        valid = True
        for script_item in self.json_data.get("script", []):
            actions = script_item.get("actions", [])
            for i, action in enumerate(actions):
                if Roles.MAIN.value in action.upper():
                    raise Exception('Main cannot be an argument in actions.')
                if action.startswith(Methods.DIALOGUE.value) and i == 0:
                    raise Exception("Invalid action sequence detected.")
                method, role = action.replace('(', ' ').replace(')', '').split()
                if role not in [role.value for role in Roles] or method not in [method.value for method in Methods]:
                    raise Exception('Invalid role or method')
        return valid

    def _validate_dialogues(self) -> bool:
        """
        Ensures all roles are uppercase in the 'dialogue' sections.

        Returns True if modifications were made, else False.
        """
        for script_item in self.json_data.get("script", []):
            for dialogue in script_item.get("dialogue", []):
                speaker = dialogue.get("speaker", "")
                if speaker != speaker.upper():
                    dialogue["speaker"] = speaker.upper()
        return True
