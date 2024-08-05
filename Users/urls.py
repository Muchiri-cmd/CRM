from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'Users'
urlpatterns = [
    path('register/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
