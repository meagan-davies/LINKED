from django.urls import path

from . import views # to import function that directs to homepage

app_name="public" # this sets all the urls to have the prefix public

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"), #route url for website
]

