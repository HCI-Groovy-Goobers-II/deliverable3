from unicodedata import name
from django.urls import path
from . import views

app_name = 'professors'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('manage_courses_and_projects/', views.manage_courses_and_projects, name='manage_courses_and_projects'),
    path('manage_courses_and_projects/<str:tab>', views.manage_courses_and_projects_tab, name='manage_courses_and_projects'),

    path('create_course/', views.create_course, name='create_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('confirm_delete_course/<int:course_id>/', views.confirm_delete_course, name='confirm_delete_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),

    path('create_project/', views.create_project, name='create_project'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('confirm_delete_project/<int:project_id>/', views.confirm_delete_project, name='confirm_delete_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('choose_project_sections/<int:project_id>/', views.choose_project_sections, name='choose_project_sections'),

    path('create_section/', views.create_section, name='create_section'),
    path('edit_section/<int:section_id>/', views.edit_section, name='edit_section'),
    path('confirm_delete_section/<int:section_id>/', views.confirm_delete_section, name='confirm_delete_section'),
    path('delete_section/<int:section_id>/', views.delete_section, name='delete_section'),
    #path('debug/', views.debug, name='debug')
]