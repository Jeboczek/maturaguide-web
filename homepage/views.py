from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

class HomePageView:
    def show_home_view(request : WSGIRequest):
        context = {
            "range": range(50)
        }
        return render(request, "home.html", context)