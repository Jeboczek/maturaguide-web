from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest

# Create your views here.

class HomePageView:
    def show_home_view(request : WSGIRequest):
        return render(request, "home.html")