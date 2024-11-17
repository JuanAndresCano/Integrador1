from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Userk
from django.utils.translation import gettext_lazy as _
from .models import Userk
from .models import Client
from .models import Freelancer
from .models import FreelancerSkillExpertise
from django.forms import ModelForm
from .models import Portfolio, Experience, Rating
from .models import Country, City
from django.core.validators import RegexValidator


class SignUpFormFreelancer(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("First Name")  # Traducción
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Last Name")  # Traducción
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Username")  # Traducción
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        label=_("Email")  # Traducción
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label=_("Password")  # Traducción
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label=_("Confirm Password")  # Traducción
    )
    identification = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Identification")  # Traducción
    )
    phoneNumber = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Phone Number")  # Traducción
    )
    
    class Meta:
        model = Userk
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'identification', 'phoneNumber']

    
class SignUpFormClient(UserCreationForm):

    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Country", widget=forms.Select(), required=True)
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="Select City", widget=forms.Select(), required=True)
    
    BUSINESS_VERTICAL_CHOICES = [
        ("Technology", "Technology"),
        ("Healthcare", "Healthcare"),
        ("Finance", "Finance"),
        ("Education", "Education"),
        ("Retail", "Retail & E-commerce"),
        ("Manufacturing", "Manufacturing"),
        ("Construction", "Construction & Real Estate"),
        ("Food & Beverage", "Food & Beverage"),
        ("Telecommunications", "Telecommunications"),
        ("Energy & Utilities", "Energy & Utilities"),
        ("Transportation & Logistics", "Transportation & Logistics"),
        ("Hospitality & Tourism", "Hospitality & Tourism"),
        ("Media & Entertainment", "Media & Entertainment"),
        ("Agriculture", "Agriculture & Agribusiness"),
        ("Government", "Government & Public Sector"),
        ("Insurance", "Insurance"),
        ("Marketing", "Marketing & Advertising"),
    ]

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("First Name*")
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label=_("Last Name*")
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label=_("Username*")
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}), 
        label=_("Email*")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), 
        label=_("Password*")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), 
        label=_("Confirm Password*")
    )
    phoneNumber = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label=_("Phone Number*"),
        validators=[RegexValidator(r'^\d+$', 'Only numeric values are allowed for phone number.')],  # Solo números
    )
    taxId = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label=_("Tax ID*"),
        validators=[RegexValidator(r'^\d+$', 'Only numeric values are allowed for phone number.')],  # Solo números
    )
    companyName = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label=_("Company Name*")
    )
    typeOfCompany = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label=_("Type of Company*")
    )
    businessVertical = forms.ChoiceField(
        choices=BUSINESS_VERTICAL_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}), 
        label=_("Business Vertical*")
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), 
        label=_("Address*")
    )

    class Meta:
        model = Userk
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phoneNumber', 
                  'taxId', 'companyName', 'typeOfCompany', 'businessVertical', 'country', 'city', 'address']
        exclude = ['profile_pic', 'description_company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # País inválido, se muestra queryset vacío
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.cities.order_by('name')
         
class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user', 'phoneNumber', 'taxId', 'companyName', 'typeOfCompany', 'businessVertical', 'country', 'city', 'address' ]

# forms.py

class FreelancerForm(forms.ModelForm):
    skillExpertises = forms.ModelMultipleChoiceField(
        queryset=FreelancerSkillExpertise.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "btn-group-toggle"}),
        required=False,
        label="Skills"
    )

    class Meta:
        model = Freelancer
        fields = '__all__'
        exclude = ['user', 'phoneNumber', 'identification', 'email']
        
    experience_level = forms.ChoiceField(
        choices=Freelancer.EXPERIENCE_LEVEL_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Experience Level"
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        required=False,
        label="Brief Description"
    )

    linkedin_url = forms.URLField(
        widget=forms.URLInput(attrs={"class": "form-control"}),
        required=False,
        label="LinkedIn URL"
    )

    github_url = forms.URLField(
        widget=forms.URLInput(attrs={"class": "form-control"}),
        required=False,
        label="GitHub URL"
    )

    instagram_url = forms.URLField(
        widget=forms.URLInput(attrs={"class": "form-control"}),
        required=False,
        label="Instagram URL"
    )

    resume = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        required=False,
        label="Upload CV"
    )


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['project_name', 'project_description', 'project_image', 'project_duration_months', 'project_link']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job', 'company', 'start_date', 'end_date', 'job_description']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': _('Type your comment here')
            }),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 3}),
        }