from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET 
from django.core.exceptions import ObjectDoesNotExist
from .generate_quiz import quiz_generator

from .models import *
from .data_presenter import *

class MaturaGuideAPIViews:
    @require_GET
    @csrf_exempt
    def get_subjects(request : WSGIRequest) -> JsonResponse:
        subjects = Subject.objects.all()
        return GetSubjectsPresenter(subjects).get_as_django_json_response()
    
    @require_GET
    @csrf_exempt
    def generate_quiz(request : WSGIRequest):
        if request.GET.get("subject_id") is None:
            return ErrorPresenter("You need to provide subject_id!").get_as_django_json_response(status_code=400)
        else:
            subject_id = request.GET["subject_id"]
        
        if request.GET.get("year") is None:
            year = 0
        else:
            year = request.GET["year"]

        return JsonResponse(quiz_generator(subject_id, year), safe=False)
        

    @require_GET
    @csrf_exempt
    def get_explanation():
        return list

    @require_GET
    @csrf_exempt
    def get_categories(request : WSGIRequest):
        if request.GET.get("subject_id") is None:
            return ErrorPresenter("You need to provide subject_id!").get_as_django_json_response(status_code=400)
        try:
            subject = Subject.objects.get(id=request.GET.get("subject_id"))
        except ObjectDoesNotExist:
            return ErrorPresenter("Can't find subject with provided id!").get_as_django_json_response(status_code=404)
        categories = QuestionCategory.objects.filter(subject = subject)
        return GetCategoriesPresenter(categories).get_as_django_json_response()