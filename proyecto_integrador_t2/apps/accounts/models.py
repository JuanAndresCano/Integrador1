from django.db import models
from django.contrib.auth.models import AbstractUser

# buily-in signals
from django.db.models.signals import post_save

#signals
from apps.notifications.signals import notificate

from django.dispatch import receiver

from django.utils import timezone

# Create your models here.
class Userk(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_freelancer = models.BooleanField('Is freelancer', default=False)
    is_client = models.BooleanField('Is client', default=False)

    #class Meta:
     #   app_label = 'accounts'

class FreelancerSkillExpertise(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    freelancer = models.ForeignKey('Freelancer', on_delete=models.CASCADE, related_name="portfolios")
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_image = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    project_duration_months = models.PositiveIntegerField()
    project_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.project_name} - {self.freelancer.user.username}"
    

class Experience(models.Model):
    freelancer = models.ForeignKey('Freelancer', on_delete=models.CASCADE, related_name="experiences")
    job = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    job_description = models.TextField()

    def __str__(self):
        return f"{self.job} at {self.company}"

class Rating(models.Model):
    freelancer = models.ForeignKey('Freelancer', on_delete=models.CASCADE, related_name='ratings')
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Rating {self.rating} by {self.client.user.username} for {self.freelancer.user.username}'
    
class Freelancer(models.Model):
    user = models.OneToOneField(Userk, on_delete=models.CASCADE, related_name="freelancer")
    phoneNumber = models.CharField(max_length=200)
    identification = models.CharField(max_length=200)
    email = models.CharField(max_length=200, default='default@example.com')
    profile_pic = models.ImageField(default='default.png', null=True, blank=True)
    skillExpertises = models.ManyToManyField(FreelancerSkillExpertise)
    EXPERIENCE_LEVEL_CHOICES = [
        ('Junior', 'Junior'),
        ('Semi-Senior', 'Semi-Senior'),
        ('Senior', 'Senior'),
    ]
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='Junior')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, null=True, blank=True)
    # Nuevos campos
    description = models.TextField(null=True, blank=True)
    linkedin_url = models.URLField(max_length=200, null=True, blank=True)
    github_url = models.URLField(max_length=200, null=True, blank=True)
    instagram_url = models.URLField(max_length=200, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Nuevo campo


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    
class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)  # Código ISO de dos letras

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name}, {self.country.name}"

class Client(models.Model):
    user = models.OneToOneField(Userk, on_delete=models.CASCADE, related_name="client")
    phoneNumber = models.CharField(max_length=200)
    taxId = models.CharField(max_length=200)
    companyName = models.CharField(max_length=200)
    typeOfCompany = models.CharField(max_length=200)
    businessVertical = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.CharField(default='', max_length=200)
    profile_pic = models.ImageField(default= 'default.png',null=True, blank=True)
    description_company = models.TextField(null=True)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

