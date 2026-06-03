import requests
import json
import re
from dotenv import load_dotenv
from os import getenv
from app.formatting import format_questions

load_dotenv()
OPENROUTER_API_KEY = getenv('OPENROUTER_API_KEY')


'''
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
'''



base_input = """You are a test writer. Make a practice multiple choice test for {subject} with {x} questions. The test MUST be a json formatted like this:

[
   {
      "question": "What is 2+2?",
      "answers": ["4", "5", "3", "2"],
      "explanation": "2+2=4"
   },
   {
      "question": "What is the capital of the United States?",
      "answers": ["Washington D.C.", "Moscow", "Paris", "Vienna"],
      "explanation": "The capital of the United States is Washington D.C."
   },
   ...
]

IMPORTANT:
 - question must be a string
 - list of answers must be list of strings with a length of 4
 - the answer must be the first item of the answer list
 - the explanation should be able to explain why an answer is correct. If the explanation requires mathematical work, use a LaTeX expression in it
 - do not add anything else to the json other what is required, under any circumstances.
 - if you are writing a mathematical expression or equation, write it in LaTeX format for MathJax compatibility so that displaying it in html is very easy.
 - You must not use single dollar sign format for LaTeX ("$...$") as it can interfere with regular dollar signs, use either "$$...$$" or "\\[...\\]" for displayed mathematics, or "\\(...\\)" for in-line mathematics.
 - You must use the <code> and <pre> html elements for coding questions to represent code
 - You must base questions from reputable sources, like CollegeBoard, code documentation, Regents or other state-wide tests, etc.

"""

def make_test_call(subject: str, question_amount: int):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "nvidia/nemotron-nano-12b-v2-vl:free",
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
    questions = re.search(r"(\[[\s\S]+\])", response['choices'][0]['message']['content'])
    questions = json.loads(questions.group(0))
    format_questions(questions)
    return questions

