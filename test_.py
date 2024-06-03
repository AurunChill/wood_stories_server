import pytest
from httpx import AsyncClient
from fastapi import status
from main import app  # Assuming the FastAPI app is defined in a file named main.py

# Sample prompts to be tested
sample_prompts = [
    {'prompt': 'Main asks wizard about necromancer', 'times': 3},
    {'prompt': 'Main speaks with knight about wizard', 'times': 3},
    {'prompt': 'Main asks wizard to find his lost keys', 'times': 3},
    {'prompt': 'Main have conflict with necromancer', 'times': 3},
]

# Define the test function
@pytest.mark.asyncio
async def test_handle_prompt():
    async with AsyncClient(app=app, base_url='http://0.0.0.0:5051') as client:
        successful_responses = 0

        for prompt in sample_prompts:
            for _ in range(prompt['times']):
                response = await client.post('/send_prompt', json=prompt)
                if response.status_code == status.HTTP_200_OK:
                    successful_responses += 1

        success_rate = successful_responses / (len(sample_prompts) * 3)  # Update this line

        assert success_rate >= 0.8, f'Success rate {success_rate * 100}% is below the expected 80%'
