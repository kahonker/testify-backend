import requests
import json
from dotenv import load_dotenv
from os import getenv

load_dotenv()
OPENROUTER_API_KEY = getenv('OPENROUTER_API_KEY')

base_input = """You are an expert in test-making, ready to make practice tests tweaked so that the user can learn most effectively.
    It needs to be in the json format:
    {
        "question number": {
            "question": question,
            "answers": {
                "0": answer
                ... and so on up to 3.
            },
            "correct_answer": index of the correct answer e.g. "0",
            "explanation": highly thorough explanation.
        }
    }
    You should use questions from reputable sources, like CollegeBoard and such.

"""

def make_test_call(subject: str, question_amount: int):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "openai/gpt-oss-120b:free",
        "messages": [
            {
            "role": "user",
            "content": f"Read this prompt {base_input}. Here is the subject: {subject} and question amount: {question_amount}"
            }
        ],
        "reasoning": {"enabled": True}
    })
    )

    # Extract the assistant message with reasoning_details
    response = response.json()
    print(response['choices'][0]['message']['content'])
    #response = response['choices'][0]['message']

