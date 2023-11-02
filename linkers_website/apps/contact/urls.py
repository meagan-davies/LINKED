from django.urls import path

from .views import contact

# url will be referenced w contact
app_name = "contact"

urlpatterns = [
    path("", contact, name="contact")
]