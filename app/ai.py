import requests
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
AI_KEY = getenv('AI_KEY')

def make_test_call(subject: str, question_amount: int):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "messages": [
            {
            "role": "user",
            "content": f"Give me {question_amount} of multiple-choice questions regarding the subject of {subject}"
            }
        ],
        "reasoning": {"enabled": True}
    })
    )
    response = response.json()
    return response['choices'][0]['message']

