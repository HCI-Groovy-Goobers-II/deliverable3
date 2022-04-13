from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as users_views
from . import views

app_name = 'public_pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('about/<str:section>', views.about_section, name='about_section'),
    path('hotjar/', views.hotjar, name='hotjar'),
    # In addition to users/login being valid URL, I'm
    # making login and accounts/login valid URLs for the
    # login page too.
    path('accounts/login/', users_views.login_view, name='login'),
    path('login/', users_views.login_view, name='login'),
]


handler404 = views.handle_404