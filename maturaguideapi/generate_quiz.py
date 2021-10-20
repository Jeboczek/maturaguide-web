from .models import Subject, Question

import random


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
