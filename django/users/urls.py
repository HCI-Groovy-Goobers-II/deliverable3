from django.urls import path, include
from django.contrib.auth import login, views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
    path('choose_app_view/', views.choose_app_view, name='choose_app_view'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('route_user', views.route_user, name='route_user'),
]