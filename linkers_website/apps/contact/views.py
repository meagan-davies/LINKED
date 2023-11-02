# import bleach
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail
from linkers_website import settings


from .forms import ContactForm

# Request made by user to access contacts.html
def contact(request: HttpRequest) -> HttpResponse: 
    
    if request.method == "GET":
        form = ContactForm()
    elif request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # extract validated fields from form
            bleach.clean(name = form.cleaned_data["name"])
            bleach.clean(email = form.cleaned_data["email"])
            bleach.clean(message = form.cleaned_data["message"])
            send_mail(f"{name} sent an email", message, email, [settings.DEFAULT_FROM_EMAIL])
            return render(request, "contact.html", {"form": form, "success": True})
    else:
        raise NotImplementedError
    
    return render(request, "contact.html", {"form": form})

# post request to recieve data from the server

