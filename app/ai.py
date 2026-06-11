import requests
import json
import re
import random
from dotenv import load_dotenv
from os import getenv
from app.formatting import format_questions
import asyncio
import httpx

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

prompt = """Generate a {x}-question multiple choice test for {subject} as a JSON array. Each object must have:"question" (string), "answers" (4 strings, first is correct), "explanation" (string). Use <code> and <pre> for code. Example:
[{{"question": "What is 2+2?", "answers": ["4", "5", "3", "2"], "explanation": "2+2=4"}}]"""

async def make_test_call(subject: str, question_amount: int):
    response = await make_test_calls(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    },
    subject=subject,
    question_amount=question_amount)
    # data=json.dumps({
    #     "model": "openai/gpt-oss-20b:free",
    #     "messages": [
    #         {
    #         "role": "user",
    #         "content": f"Read this prompt {base_input}. Here is the subject: {subject} and question amount: {question_amount}"
    #         }
    #     ],
    #     "reasoning": {"enabled": True},
    #     "response_format": { "type": "json_object" },
    #     "temperature": 0.8,
    #     "top_p": 0.9,
    #     "top_k": 45,
    #     "frequency_penalty": 0.2,
    #     "presence_penalty": 0.2
    # })
    # )

    # Extract the assistant message with reasoning_details
    # response = response.json()
    # print(response)
    # questions = re.search(r"(\[[\s\S]+\])", response['choices'][0]['message']['content'])
    # questions = json.loads(questions.group(0))
    # format_questions(questions)
    response = format_questions(response)
    return response

async def make_test_calls(url, headers, subject, question_amount):
    data_list = []
    for i in range(int(question_amount/5)):
        data_list.append({
        "model": "google/gemini-2.5-flash-lite",
        "messages": [
            {
            "role": "user",
            "content": prompt.format(x = 5, subject=subject)
            }
        ],
        "response_format": { "type": "json_object" },
        "temperature": 0.8,
        "top_p": 0.9,
        "top_k": 45,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.2,
    })

    response_list = []
    async with httpx.AsyncClient() as client:
        tasks = [await client.post(url, headers=headers, data=json.dumps(data)) for data in data_list]
    
    for task in tasks:
        try:
            questions = task.json()['choices'][0]['message']['content']
            questions = json.loads(questions)
            response_list = response_list + questions
        except Exception as e:
            print(questions)
            continue

    return response_list

