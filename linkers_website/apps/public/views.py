'''
Python functions that take http requests and return http reponses
'''

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Request made by user to access index.html
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

# Request made by user to access about.html
def about(request: HttpRequest) -> HttpResponse:
    return render(request, "about.html")

