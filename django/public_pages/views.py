from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime as dt, timedelta
from .models import HotJar
from .forms import HotJarForm


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

def hotjar(request):
    hotjar = HotJar.objects.get(id=1)
    if not request.method == 'POST':
        form = HotJarForm(instance=hotjar)
    else:
        form = HotJarForm(instance=hotjar, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('public_pages:index'))

    return render(request, 'public_pages/hotjar.html', context={ 'form': form })
