from random import shuffle

def format_questions(questions):
    for question in questions:
        correct = question.get("answers")[0]
        shuffle(question.get("answers"))
        question["correct"] = question.get("answers").index(correct)
        question["answered"] = -1
