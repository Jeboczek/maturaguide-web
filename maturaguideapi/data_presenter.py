from django.http import JsonResponse

from typing import List
import json
from .models import *

class Presenter():
    def get_as_object(self) -> list:
        return []

    def get_as_json(self) -> str:
        return json.encoder(self.get_as_object())

    def get_as_django_json_response(self) -> JsonResponse:
        return JsonResponse(self.get_as_object(), safe=False)

    def __str__(self) -> str:
        return self.get_as_json()

class GetSubjectsPresenter(Presenter):
    def __init__(self, subjects : List[Subject]) -> None:
        self.subjects = subjects
    
    def get_as_object(self) -> list:
        return [{"id": subject.id, "name": subject.name, "total_questions": subject.count_questions()} for subject in self.subjects]