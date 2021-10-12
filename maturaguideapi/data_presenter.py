from django.http import JsonResponse

from typing import List
import json
from .models import *

class Presenter():
    def get_as_object(self) -> list:
        return []

    def get_as_json(self) -> str:
        return json.encoder(self.get_as_object())

    def get_as_django_json_response(self, status_code=200) -> JsonResponse:
        return JsonResponse(self.get_as_object(), safe=False, status=status_code)

    def __str__(self) -> str:
        return self.get_as_json()

class ErrorPresenter(Presenter):
    def __init__(self, message : str) -> None:
        self.message = message
    
    def get_as_object(self) -> list:
        return {"error": 1, "error_message": self.message}
class GetSubjectsPresenter(Presenter):
    def __init__(self, subjects : List[Subject]) -> None:
        self.subjects = subjects
    
    def get_as_object(self) -> list:
        return [{"id": subject.id, "name": subject.name, "total_questions": subject.count_questions(), "type": subject.subject_type} for subject in self.subjects]

class GetCategoriesPresenter(Presenter):
    def __init__(self, categories : List[QuestionCategory]) -> None:
        self.categories = categories

    def get_as_object(self) -> list:
        return [{"id": category.id, "name": category.name, "total_questions": category.count_questions()} for category in self.categories]

class GetExplanationPresenter(Presenter):
    def __init__(self, explanations : List[str], question_nr : int) -> None:
        self.explanations = explanations
        self.question_nr = question_nr

    def get_as_object(self) -> dict:
        return_dict = {}
        [return_dict.update({f"{self.question_nr}.{i}": explanation}) for i, explanation in enumerate(self.explanations, start=1)]
        return return_dict