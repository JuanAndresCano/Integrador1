from django.urls import path 
from . import views

urlpatterns = [
    path('dashboardFreelancer/', views.dashboardFreelancer, name="dashboardFreelancer"),
    path('dashboardClient/', views.dashboardClient, name="dashboardClient"),
    path('clientAnalysis/', views.clientAnalysis, name='clientAnalysis'),
    path('freelancerAnalysis/', views.freelancerAnalysis, name='freelancerAnalysis'),

]