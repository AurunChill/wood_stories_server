# Third-party
from openai import AsyncOpenAI

# Standard
from datetime import datetime, timezone, timedelta

# Project
from logger import gpt_logger
import config as cf


_client = AsyncOpenAI(
    api_key=cf.gpt['api_key'],
    base_url=cf.gpt['base_url'],
)


async def send_gpt(prompt: str) -> dict:
    """Function that sends a prompt to OpenAI's Chat endpoint and parses the response.

    Args:
        prompt (str): The input prompt to send.

    Returns:
        dict: A dictionary containing relevant details about the transaction and response.
    """

    # Log the information about the prompt being sent to the OpenAI model
    gpt_logger.info(f'Requesting response from {cf.gpt["model"]} with prompt: {prompt}')

    # Create the completion request to OpenAI's Chat endpoint.
    response_data = await _client.chat.completions.create(
        model=cf.gpt['model'],
        messages=[{'role': cf.gpt['role'], 'content': prompt}],
    )

    # Record the current transaction time.
    transaction_time = datetime.now(timezone(timedelta(hours=3)))

    # Extract the prompt and completion token count from the API response.
    prompt_tokens = response_data.usage.prompt_tokens
    completion_tokens = response_data.usage.completion_tokens

    # Calculate the price of the prompt and completion based on known token prices.
    prompt_price = round((cf.gpt['input_price'] / 1000) * prompt_tokens, 5)
    completion_price = round((cf.gpt['output_price'] / 1000) * completion_tokens, 5)
    
    # Construct and return a dictionary containing various transaction details.
    response_data = {
        'transaction_time': str(transaction_time),
        'user_role': cf.gpt['role'],
        'model': cf.gpt['model'],
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': prompt_tokens + completion_tokens,
        'prompt_price': prompt_price,
        'completion_price': completion_price,
        'total_price': round(prompt_price + completion_price, 5),
        'prompt': prompt,
        'response': response_data.choices[0].message.content,
    }

    # Log the response details received
    gpt_logger.info(f'Response received: {response_data}')
    
    return response_data