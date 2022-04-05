from django.urls import path
from . import views

app_name = 'professors'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_course/', views.create_course, name='create_course'),
    path('create_project/', views.create_project, name='create_project'),
    path('create_section/', views.create_section, name='create_section'),
    path('debug/', views.debug, name='debug')                      
]