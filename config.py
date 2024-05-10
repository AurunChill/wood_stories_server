# Third-party
from dotenv import load_dotenv

# Standard
import os
import pathlib


# Get the base path of the current file
BASE_PATH = pathlib.Path(__file__).resolve().parent

# Get the templates path
TEMPLATE_PATH = BASE_PATH / 'templates'

# Load environment variables from a .env file
load_dotenv(BASE_PATH / ".env")

# Define a dictionary containing configuration settings for the GPT model
# Information about models and prices is here: https://proxyapi.ru/pricing
gpt = {
    "api_key": os.getenv("OPENAI_KEY"),  # Get the OpenAI API key
    "model": "gpt-3.5-turbo-0125",  # Define the version of the GPT model
    "role": "user",  # Define the role as user
    "base_url": "https://api.proxyapi.ru/openai/v1",  # Define the base URL for the API
    "input_price": 0.144,  # Define the input price
    "output_price": 0.432,  # Define the output price
}
