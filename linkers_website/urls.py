"""
Define URL routes 

URL configuration for linkers_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views



from . import views # to import function that directs to homepage


urlpatterns = [
    path("", include('linkers_website.apps.public.urls')),
    path("admin/", admin.site.urls),
    path("contact/", include('linkers_website.apps.contact.urls')),
    path("linkers/", include('linkers_website.apps.Linker.urls')),
    path("calculator/", include('linkers_website.apps.calculator.urls')),

]

