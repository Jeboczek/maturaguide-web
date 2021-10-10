from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET 
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .generate_quiz import quiz_generator

from .models import *
from .data_presenter import *

def get_subject_by_provided_subject_id(request : WSGIRequest) -> Subject:
    if request.GET.get("subject_id") is None:
        raise ValidationError("You need to provide subject_id!")
    try:
        subject = Subject.objects.get(id=request.GET.get("subject_id"))
        return subject
    except ObjectDoesNotExist:
        raise ValidationError("Can't find subject with provided id!")
class MaturaGuideAPIViews:
    @require_GET
    @csrf_exempt
    def get_subjects(request : WSGIRequest) -> JsonResponse:
        subjects = Subject.objects.all()
        return GetSubjectsPresenter(subjects).get_as_django_json_response()
    
    @require_GET
    @csrf_exempt
    def generate_quiz(request : WSGIRequest):
        try:
            subject = get_subject_by_provided_subject_id(request)
        except ValidationError as e:
            return ErrorPresenter(e.message).get_as_django_json_response(status_code=400)

        year = 0 if request.GET.get("year") is None else request.GET.get("year")

        return JsonResponse(quiz_generator(subject, year), safe=False)
        

    @require_GET
    @csrf_exempt
    def get_explanation():
        return list

    @require_GET
    @csrf_exempt
    def get_categories(request : WSGIRequest):
        try:
            subject = get_subject_by_provided_subject_id(request)
        except ValidationError as e:
            return ErrorPresenter(e.message).get_as_django_json_response(status_code=400)

        categories = QuestionCategory.objects.filter(subject = subject)
        return GetCategoriesPresenter(categories).get_as_django_json_response()