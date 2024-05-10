# Third-party
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Project
from gpt import send_gpt
import script_manager as s_manager
from script_manager import Templates
from validator import JSONValidator

# Initialize a FastAPI application
app = FastAPI()

# Request data model
class PromptModel(BaseModel):
    prompt: str

# Define a POST route to handle incoming prompts
@app.post("/send_prompt")
async def handle_prompt(prompt_model: PromptModel):
    """
    Handles incoming prompts provided by clients, sends them to GPT model for processing, and returns the generated result.

    Args:
        prompt_model (PromptModel): Request body containing the prompt to be processed.

    Raises:
        HTTPException: If the request data is invalid or the 'prompt' field is missing.

    Returns:
        dict: JSON response containing the result of the GPT model processing.
    """
    try:
        # Perform script processing on the prompt
        base_prompt = await s_manager.scriptize_prompt(prompt=prompt_model.prompt, template=Templates.NEW)

        # Send the base prompt to the GPT model
        temp_result = await send_gpt(prompt=base_prompt)

        # # Expand the prompt based on the model response
        # expanded_prompt = await s_manager.scriptize_prompt(prompt=temp_result['response'], template=Templates.EXPAND)

        # # Send the expanded prompt for processing
        # result = await send_gpt(expanded_prompt)

        # Validate the response
        validator = JSONValidator(json_data=temp_result['response'])
        validated_result = validator.validate_and_modify_json()

        if isinstance(validated_result, str):
            raise HTTPException(status_code=500, detail='Invalid generation\n' + validated_result)

        # Return the validated JSON response
        return validated_result
    
    # Handle exceptions that occur during processing
    except Exception as e:
        # Raise an HTTP exception with an error message
        raise HTTPException(status_code=400, detail=str(e))
    

    # COME_TO WIZARD