"""maturaguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from contact.views import ContactView
from maturaguideapi.views import MaturaGuideAPIViews
from homepage.views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomePageView.show_home_view ),
    path('o-nas/', HomePageView.show_aboutus_view ),
    path('kontakt/', ContactView.show_root),
    path('kontakt/success', ContactView.show_success),

    # API
    path('api/get_subjects', MaturaGuideAPIViews.get_subjects),
    path('api/generate_quiz', MaturaGuideAPIViews.generate_quiz),
    path('api/get_categories', MaturaGuideAPIViews.get_categories),
    path('api/get_cke_sheets', MaturaGuideAPIViews.get_cke_sheets),
]
