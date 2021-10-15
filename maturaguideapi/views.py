from django.db.models.base import Model
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .generate_quiz import quiz_generator

from .models import *
from .data_presenter import *


def get_object_by_provided_object_id(
    request: WSGIRequest, key: str, model_class: Model
) -> Model:
    if request.GET.get(key) is None:
        raise ValidationError(f"You need to provide {key}!")
    try:
        object = model_class.objects.get(id=request.GET.get(key))
        return object
    except ObjectDoesNotExist:
        raise ValidationError(f"Can't find {model_class.__name__} with provided id!")


class MaturaGuideAPIViews:
    @require_GET
    @csrf_exempt
    def get_subjects(request: WSGIRequest) -> JsonResponse:
        subjects = Subject.objects.all()
        return GetSubjectsPresenter(subjects).get_as_django_json_response()

    @require_GET
    @csrf_exempt
    def get_cke_sheets(request: WSGIRequest) -> JsonResponse:
        try:
            subject = get_object_by_provided_object_id(request, "subject_id", Subject)
        except ValidationError as e:
            return ErrorPresenter(e.message).get_as_django_json_response(
                status_code=400
            )
        return JsonResponse(
            list(
                set(
                    [
                        question.cke_year
                        for question in Question.objects.filter(subject=subject)
                    ]
                )
            ),
            safe=False,
        )

    @require_GET
    @csrf_exempt
    def generate_quiz(request: WSGIRequest):
        try:
            excercise = get_object_by_provided_object_id(request, "subject_id", Subject)
        except ValidationError as e:
            return ErrorPresenter(e.message).get_as_django_json_response(
                status_code=400
            )

        year = 0 if request.GET.get("year") is None else request.GET.get("year")

        return JsonResponse(quiz_generator(excercise, year), safe=False)

    @require_GET
    @csrf_exempt
    def get_categories(request: WSGIRequest):
        try:
            subject = get_object_by_provided_object_id(request, "subject_id", Subject)
        except ValidationError as e:
            return ErrorPresenter(e.message).get_as_django_json_response(
                status_code=400
            )

        categories = subject.get_categories()
        return GetCategoriesPresenter(categories).get_as_django_json_response()
