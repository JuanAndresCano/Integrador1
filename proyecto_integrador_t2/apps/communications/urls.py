from django.urls import path 
from . import views

urlpatterns = [
    path('freelancerMessageHome/', views.freelancerMessageHome, name="freelancerMessageHome"),
    path('clientMessageHome/', views.clientMessageHome, name="clientMessageHome"),
    path('freelancerMessage/<chatName>', views.freelancerMessage, name="freelancerMessage"),
    path('clientMessage/<chatName>', views.clientMessage, name="clientMessage"),
    path('clientCreateComprobateChat/<str:username>', views.clientCreateComprobateChat, name="clientCreateComprobateChat"),
    path('freelancerCreateComprobateChat/<str:username>', views.freelancerCreateComprobateChat, name="freelancerCreateComprobateChat"),
]