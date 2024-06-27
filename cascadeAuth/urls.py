from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),

   path('register/', views.register, name="register"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('activation_success/', views.activation_success, name='activation_success'),
    path('activation_invalid/', views.activation_invalid, name='activation_invalid'),

    path('login/', views.login, name='login'),
    
    path('otp/', views.otp, name="otp"),
    path('captcha/', views.captcha, name="captcha"),
    
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='cascadeAuth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.resetPassword, name='resetPassword'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='cascadeAuth/password_reset_complete.html'), name='password_reset_complete'),
    
    path('dashboard/', views.dashboard, name="dashboard"),
    
    path('logout/', views.logout, name='logout'),
]