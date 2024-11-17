from django.db import models
from apps.accounts.models import Freelancer, Client
from datetime import timedelta, timezone 
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notifications.signals import notificate


# Create your models here.

class ProjectSkillExpertise(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ProjectComplexity(models.Model):
    levelName = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.levelName

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    datePosted = models.DateTimeField(auto_now_add=True)
    requiredPosition = models.CharField(max_length=200)
    daysDuration = models.IntegerField(null=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    skillExpertises = models.ManyToManyField(ProjectSkillExpertise)
    complexity = models.ForeignKey(ProjectComplexity, on_delete=models.CASCADE, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    version = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title
    
    @property
    def progress(self):
        # Obtener todos los `ProjectContributor` asociados al proyecto
        contributors = self.projectContributor.all()
        
        # Si no hay contributors, el progreso es 0
        if not contributors.exists():
            return 0

        # Calcular el promedio del progreso de cada contributor
        total_progress = sum(contributor.progress for contributor in contributors)
        return round(total_progress / contributors.count())  # Redondear el progreso total

class ProjectContributor(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    requiredPosition = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    daysDuration = models.IntegerField(null=True)
    complexity = models.ForeignKey(ProjectComplexity, on_delete=models.CASCADE, null=True)
    startDate = models.DateTimeField(null=True, blank=True) # asignar cuando se acepte en notificaciones
    version = models.IntegerField()
    endDate = models.DateField(null=True, blank=True)
    PROJECT_STATUS_CHOICES = (
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('OVERDUE', 'Overdue'),
        ('PENDING', 'Pending'),
    )
    project_status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='PENDING')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='projectContributor')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, null=True, related_name='freelancer')
    APPROVED_STATES = (
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('not_rejected', 'Not rejected'),
        ('pending', 'Pending'),
    )
    approval_status = models.CharField(max_length=25, choices=APPROVED_STATES, default='pending')
    REJECT_REASON = (
        ('profile_rejected', 'Rejected due to profile'),
        ('deliverables_rejected', 'Rejected due to deliverables'),
        ('not_rejected', 'Not rejected'),
        ('pending', 'Pending')
    )
    rejectionReason = models.CharField(max_length=30, choices=REJECT_REASON, default='pending')    
    is_send = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    finishJob = models.BooleanField(default=False) #Para hacer lo de pasarela de pagos de Tomas
    payment_completed = models.BooleanField(default=False) 
    # Propiedad para calcular el progreso
    
    @property
    def progress(self):
        # Obtener todos los milestones del ProjectContributor
        milestones = self.milestones.all()
        
        # Obtener todos los deliverables asociados a estos milestones
        deliverables = Deliverable.objects.filter(milestone__in=milestones)
        
        # Calcular el total de deliverables
        total_deliverables = deliverables.count()
        
        # Si no hay deliverables, el progreso es 0
        if total_deliverables == 0:
            return 0
        
        # Contar los deliverables que están completos
        completed_deliverables = deliverables.filter(done=True).count()

        # Calcular el porcentaje de progreso y redondearlo
        return round((completed_deliverables / total_deliverables) * 100)
    
    def __str__(self):
        return f'{self.title} - {self.freelancer}'

class Milestone(models.Model):
    name = models.CharField(max_length=200)
    projectContributor = models.ForeignKey(ProjectContributor, on_delete=models.CASCADE, related_name='milestones', null=True)
    def __str__(self):
        return self.name

class Deliverable(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    deadlineInDays = models.IntegerField()
    requiresEvidence = models.BooleanField()
    done = models.BooleanField(default=False)
    evidenceFile = models.FileField(upload_to='evidence_files/', null=True, blank=True)
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='deliverables', null=True)
    awaiting_approval = models.BooleanField(default=False)  # Indica si está en espera de aprobación del cliente
    approval_requested = models.BooleanField(default=False)  # Para controlar si se ha solicitado aprobación

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    project_contributor = models.ForeignKey(ProjectContributor, on_delete=models.CASCADE, related_name='transactions')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='transactions')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='received_transactions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Transaction {self.id} - {self.project.title} - {self.amount} - {self.status}'
    