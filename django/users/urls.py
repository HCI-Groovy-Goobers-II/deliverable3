from django.urls import path, reverse_lazy
from django.urls import path, include
from django.contrib.auth import login, views as auth_views
from . import views
from .forms import CustomSetPasswordForm

app_name = 'users'
urlpatterns = [
    path('choose_app_view/', views.choose_app_view, name='choose_app_view'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('route_user/', views.route_user, name='route_user'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
			template_name='users/password_reset/reset_password_email.html',
			email_template_name='users/password_reset/reset_email_message.html',
			success_url=reverse_lazy('users:password_reset_sent'),
		), name='reset_password'),

	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
			template_name='users/password_reset/reset_password_sent.html'), name='password_reset_sent'),

	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            form_class=CustomSetPasswordForm,
			template_name='users/password_reset/reset_password_confirm.html',
			success_url=reverse_lazy('users:password_reset_complete'),
		), name='password_reset_confirm'),

	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
			template_name='users/password_reset/reset_password_complete.html'), name='password_reset_complete')
]