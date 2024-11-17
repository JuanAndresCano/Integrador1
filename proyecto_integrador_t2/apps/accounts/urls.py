from django.urls import path 

from django.contrib.auth import views as auth_views

from django.urls import path, re_path
from . import views
from .views import client_profile

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('', views.landpage, name='landpage'),
    path('freelancerRegister/', views.freelancerRegister, name='freelancerRegister'),
    path('clientRegister/', views.clientRegister, name='clientRegister'),
    path('logout/', views.logout, name='logout'),
    path('profile/', client_profile, name='clientProfile'),  # Esto muestra el perfil del cliente
    path('fprofile/<int:pk>/', views.freelancer_profile, name='freelancerProfile'),
    path('fprofileRequest/<str:pk>/<str:contributorId>/', views.fprofileRequest, name='fprofileRequest'),
    path('fprofileSettings/', views.freelancer_profile_settings, name='freelancerProfileSettings'),
    path('fprofileSettings/delete-portfolio/<int:portfolio_id>/', views.delete_portfolio, name='delete_portfolio'),
    path('recoverPassword/', 
         auth_views.PasswordResetView.as_view(template_name="accounts/recoverPassword.html"), 
         name='recoverPassword'),
    path('recoverPasswordSent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/recoverPasswordSent.html"), 
         name='password_reset_done'),
    path('recover/<uidb64>/<token>', 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/recoverPasswordForm.html"), 
         name='password_reset_confirm'),
    path('recoverPasswordDone/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/recoverPasswordDone.html"), 
         name='password_reset_complete'),
     
     path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

]
          