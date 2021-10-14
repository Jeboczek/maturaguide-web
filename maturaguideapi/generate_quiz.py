from .models import Subject, Question

import random

# def assign_a_question_and_answer_numbers(question : dict, number : str) -> dict:
#     """A function that assigns numbers to questions and answers """
#     question["question_nr"] = number
#     answers = []
#     for i, answer in enumerate(question["answers"], start=1):
#         answer["answer_id"] = number + f".{i}"
#         answers.append(answer)
#     question["answers"] = answers
#     return question 

def quiz_generator(subject : Subject, year=0, question_limit=9) -> list:
    """Function for generating quizzes.
    The year attribute can be set to 0 to get a randomly generated sheet."""
    if year == 0:
        questions = Question.objects.filter(subject=subject)
        # Shuffle questions
        questions = sorted(questions, key=lambda x: random.random())
    else:
        questions = Question.objects.filter(year=year, subject=subject)
        # Sort all question by cke_order
        questions = sorted(questions, key = lambda x: x.cke_order)
    
    questions = questions[:question_limit]

    sheet = []
    for i, question in enumerate(questions, start=1):
        sheet.append((question.get_as_object(str(i))))
    return sheet
