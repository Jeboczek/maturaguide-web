from .models import Subject, Question

def assign_a_question_and_answer_numbers(question : dict, number : str) -> dict:
    question["question_nr"] = number
    answers = []
    for i, answer in enumerate(question["answers"], start=1):
        answer["answer_id"] = number + f".{i}"
        answers.append(answer)
    question["answers"] = answers
    return question 

def quiz_generator(subject_id, year=0) -> list:
    """Function for generating quizzes.
    The year attribute can be set to 0 to get a randomly generated sheet."""
    if year == 0:
        # TODO: Get random questions
        raise NotImplementedError()
    else:
        subject = Subject.objects.get(id=subject_id)
        questions = Question.objects.filter(year=year, subject=subject)
        # Sort all question by cke_order
        questions = sorted(questions, key = lambda x: x.cke_order)
    
    sheet = []
    for i, question in enumerate(questions, start=1):
        sheet.append(assign_a_question_and_answer_numbers(question.get_as_object(), str(i)))
    return sheet
