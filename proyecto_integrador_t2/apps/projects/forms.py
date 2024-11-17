from django import forms
from django.forms import ModelForm
from .models import Project, Deliverable, Milestone


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['client', 'version']

class DeliverableForm(forms.ModelForm):
    class Meta:
        model = Deliverable
        fields = ['name', 'description', 'deadlineInDays', 'requiresEvidence']


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['name']
        