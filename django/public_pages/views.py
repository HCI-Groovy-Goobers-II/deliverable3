from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime as dt, timedelta


def handle_404(request, exception):
    return render(request, '404.html', context={})

def index(request):
    return render(request, 'public_pages/index.html', context={})

def about(request):
    return render(request, 'public_pages/about.html', context={})

def about_section(request, section):
    """Template script will go to the section with the ID that matches the section arg."""
    return render(request, 'public_pages/about.html',
                    context={ 'goto_section': section })
