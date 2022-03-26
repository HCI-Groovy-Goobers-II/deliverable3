from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from datetime import datetime as dt, timedelta


def handle_404(request, exception):
    return render(request, '404.html', context={})

def index(request):
    return render(request, 'public_pages/index.html', context={})
