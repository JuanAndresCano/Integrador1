import django_filters
from django_filters import DateFilter, NumberFilter, CharFilter
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import *

class BrowseProjectFilter(django_filters.FilterSet):
    min_budget = NumberFilter(field_name='budget', lookup_expr='gte', label=_('Minimum Budget'))
    max_budget = NumberFilter(field_name='budget', lookup_expr='lte', label=_('Maximum Budget'))
    title = CharFilter(field_name='title', lookup_expr='icontains', label=_('Search by Title'))
    position = CharFilter(field_name='requiredPosition', lookup_expr='icontains', label=_('Search by Position'))
    
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['description', 'daysDuration', 'datePosted', 'budget', 'title', 'requiredPosition', 'client', 'complexity', 'skillExpertises', 'version']

class ProjectFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label=_('Search by Title'))
    position = CharFilter(field_name='requiredPosition', lookup_expr='icontains', label=_('Search by Position'))
    
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['description', 'daysDuration', 'datePosted', 'budget', 'title', 'requiredPosition', 'client', 'complexity', 'skillExpertises', 'version']  
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'title' in self.form.fields:
            self.form.fields['title'].widget = forms.HiddenInput()