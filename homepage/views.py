from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

class HomePageView:
    def show_home_view(request : WSGIRequest):
        context = {
            "range": range(50),
            "title": "Maturzystnie",
            "category": "home",
        }
        return render(request, "home.html", context)

    def show_aboutus_view(request : WSGIRequest):
        context = {
            "title": "O nas - Maturzystnie",
            "category": "aboutus",
        }
        return render(request, "aboutus.html", context)