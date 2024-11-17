from django import forms
from django.forms import ModelForm
from .models import *


class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        
