from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import allowed_users
from apps.projects.models import Project, ProjectContributor
from apps.accounts.models import Client, Freelancer
from apps.communications.models import Chat, Message
from django.db.models import Subquery, OuterRef, Value
from django.db.models.functions import Concat
import json
from django.db.models import Count, Q
from datetime import datetime
from django.db.models.functions import Substr


@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def dashboardFreelancer(request):
    user = request.user

    # Obtener los proyectos del freelancer a través de ProjectContributor
    projects = Project.objects.filter(projectContributor__freelancer=request.user.freelancer).order_by('-datePosted')[:5]

    # Obtener los últimos 5 chats del freelancer actual y su último mensaje
    latest_chats = Chat.objects.filter(freelancer=request.user.freelancer).order_by('-id')[:5]
    last_message_subquery = Message.objects.filter(chat=OuterRef('pk')).order_by('-timeCreated').values('body')[:1]
    last_message_subquery = last_message_subquery.annotate(short_body=Substr('body', 1, 80)).values('short_body')
    latest_chats = latest_chats.annotate(last_message=Subquery(last_message_subquery),other_user_name=Concat('client__user__first_name', Value(' '), 'client__user__last_name'))

     # Obtener el saldo del freelancer y sus últimas tres transacciones
    freelancer = request.user.freelancer
    balance = freelancer.balance
    transactions = freelancer.received_transactions.order_by('-transaction_date')[:3]
    
    # Pasamos la información completa del cliente para obtener el nombre y perfil en el template
    context = {
        'user_name': user.first_name,
        'projects': projects,
        'latest_chats': latest_chats,
        'balance': balance,
        'transactions': transactions,
    }

    return render(request, 'dashboard/dashboardFreelancer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def dashboardClient(request):
    user = request.user
    client = request.user.client

    # Obtener los proyectos del cliente
    projects = Project.objects.filter(client=client).order_by('-datePosted')[:5]

    # Obtener los últimos 5 chats del cliente actual y su último mensaje
    latest_chats = Chat.objects.filter(client=client).order_by('-id')[:5]
    last_message_subquery = Message.objects.filter(chat=OuterRef('pk')).order_by('-timeCreated').values('body')[:1]
    last_message_subquery = last_message_subquery.annotate(short_body=Substr('body', 1, 80)).values('short_body')
    latest_chats = latest_chats.annotate(
        last_message=Subquery(last_message_subquery),
        other_user_name=Concat('freelancer__user__first_name', Value(' '), 'freelancer__user__last_name')
    )

    # Obtener las transacciones del cliente
    completed_transactions = client.transactions.filter(status='completed').order_by('-transaction_date')[:3]
    pending_transactions = client.transactions.filter(status='pending').order_by('-transaction_date')[:3]
    completed_count = completed_transactions.count()
    pending_count = pending_transactions.count()

    context = {
        'user_name': user.first_name,
        'projects': projects,
        'latest_chats': latest_chats,
        'completed_transactions': completed_transactions,
        'pending_transactions': pending_transactions,
        'completed_count': completed_count,
        'pending_count': pending_count,
    }

    return render(request, 'dashboard/dashboardClient.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def clientAnalysis(request):
    projects = Project.objects.filter(client=request.user.client)
    
    # Títulos y progreso de proyectos (anterior)
    project_titles = [project.title for project in projects]
    project_progress = [project.progress for project in projects]

    # Complejidad de proyectos (anterior)
    complexity_data = (
        projects.values('complexity__levelName')
        .annotate(total=Count('complexity'))
        .order_by('complexity__levelName')
    )
    complexity_labels = [entry['complexity__levelName'] for entry in complexity_data]
    complexity_counts = [entry['total'] for entry in complexity_data]

    # Entregables completados y pendientes para cada proyecto
    deliverables_completed = [
        project.projectContributor.aggregate(
            completed=Count('milestones__deliverables', filter=Q(milestones__deliverables__done=True))
        )['completed'] or 0 for project in projects
    ]
    
    deliverables_pending = [
        project.projectContributor.aggregate(
            pending=Count('milestones__deliverables', filter=Q(milestones__deliverables__done=False))
        )['pending'] or 0 for project in projects
    ]

    context = {
        'project_titles': json.dumps(project_titles),
        'project_progress': json.dumps(project_progress),
        'complexity_labels': json.dumps(complexity_labels),
        'complexity_counts': json.dumps(complexity_counts),
        'deliverables_completed': json.dumps(deliverables_completed),
        'deliverables_pending': json.dumps(deliverables_pending),
    }
    return render(request, 'dashboard/clientAnalysis.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def freelancerAnalysis(request):
    # Distribución de Tiempo en Proyectos Actuales
    time_distribution = []
    for contributor in ProjectContributor.objects.filter(freelancer=request.user.freelancer, project_status='IN_PROGRESS'):
        elapsed_days = (datetime.now().date() - contributor.startDate.date()).days if contributor.startDate else 0
        remaining_days = max(contributor.daysDuration - elapsed_days, 0)
        time_distribution.append({
            'title': contributor.project.title,
            'elapsed_days': elapsed_days,
            'remaining_days': remaining_days
        })

    # Progreso de Entregables por Proyecto
    project_progress = []
    project_titles = []
    for contributor in ProjectContributor.objects.filter(freelancer=request.user.freelancer):
        project_titles.append(contributor.project.title)
        project_progress.append(contributor.progress)

    # Éxito en la Finalización de Proyectos
    success_rates = []
    completion_dates = []
    for contributor in ProjectContributor.objects.filter(freelancer=request.user.freelancer, project_status='DONE'):
        if contributor.endDate and contributor.startDate:
            total_days = (contributor.endDate - contributor.startDate.date()).days
            success_rate = 1 if total_days <= contributor.daysDuration else 0
            success_rates.append(success_rate)
            completion_dates.append(contributor.endDate.strftime("%Y-%m-%d"))

    # Complejidad de Proyectos
    complexity_data = (
        ProjectContributor.objects.filter(freelancer=request.user.freelancer)
        .values('project__complexity__levelName')
        .annotate(total=Count('project__complexity'))
        .order_by('project__complexity__levelName')
    )
    complexity_labels = [entry['project__complexity__levelName'] for entry in complexity_data]
    complexity_counts = [entry['total'] for entry in complexity_data]

    context = {
        'time_distribution': json.dumps(time_distribution),
        'project_titles': json.dumps(project_titles),
        'project_progress': json.dumps(project_progress),
        'complexity_labels': json.dumps(complexity_labels),
        'complexity_counts': json.dumps(complexity_counts),
        'completion_dates': json.dumps(completion_dates),
        'success_rates': json.dumps(success_rates),
    }
    return render(request, 'dashboard/freelancerAnalysis.html', context)