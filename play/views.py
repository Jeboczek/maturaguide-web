from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.

class PlayViews:
    def show_root(request : WSGIRequest):
        context = {
            "category": "learn",
        }
        return render(request, "play.html", context)