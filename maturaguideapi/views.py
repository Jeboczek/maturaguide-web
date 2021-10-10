from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET 

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
    def generate_quiz():
        return list

    @require_GET
    @csrf_exempt
    def get_explanation():
        return list

    @require_GET
    @csrf_exempt
    def get_categories():
        return list