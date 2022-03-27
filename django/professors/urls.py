from django.urls import path
from . import views

app_name = 'professors'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]