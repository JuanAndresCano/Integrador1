from decimal import Decimal
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import Template, Context
from django.forms import inlineformset_factory
from django.utils import timezone
from django.urls import reverse
from proyecto_integrador_t2 import settings
from .models import *
from .forms import *
from .filters import *
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import allowed_users
from django.contrib import messages
from apps.notifications.signals import notificate
from django.shortcuts import render
from django.db.models import Sum, Q, Count



# Create your views here.
#CLIENT------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def createProject(request):
    form = ProjectForm()
    totalProjects = Project.objects.filter(client=request.user.client).count()
    update = False
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.client = request.user.client
            project.save()
            form.save_m2m()  # Guarda las relaciones ManyToMany (habilidades seleccionadas)
            messages.success(request, "Project created successfully.")
            return redirect('clientProject')
        else:
            messages.error(request, "Error creating project. Please check the form.")
    context = {'form':form,
               'totalProjects' : totalProjects,
               'update' : update}
    return render(request, 'projects/client/createProject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def updateProject(request, pk):

    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    totalProjects = Project.objects.filter(client=request.user.client).count()
    update = True

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.version += 1
            project.save()
            form.save_m2m()  # Asegúrate de guardar las habilidades seleccionadas al actualizar
            messages.success(request, "Project updated successfully.")
            return redirect('clientProject')
        else:
            messages.error(request, "Error updating project. Please check the form.")
    context = {'form':form,
               'totalProjects' : totalProjects,
               'update' : update}
    return render(request, 'projects/client/createProject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def clientProject(request):
    client = request.user.client

    myFilter = ProjectFilter(request.GET, queryset=Project.objects.filter(client=client))

    projects = myFilter.qs

    sort_by = request.GET.get('sort_by', '-datePosted')
    projects = projects.order_by(sort_by)

    projects = projects[:15]

    context = {
        'projects': projects,
        'myFilter': myFilter,
        'sort_by': sort_by
    }
       

    return render(request, 'projects/client/clientProject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def listFreelancer(request, pk):
    project = Project.objects.get(id=pk)
    projectContributors = project.projectContributor.filter(is_send=True, approval_status='approved')

    context = {'project':project,
               'projectContributors':projectContributors}

    return render(request, 'projects/client/listFreelancer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def clientDeliverable(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)
    client = request.user.client
    milestones = projectContributor.milestones.all()
    skills = projectContributor.project.skillExpertises.all()

    if request.method == 'POST':
        if 'finish_job' in request.POST:
            # Cambia el estado de finishJob solo si todos los entregables están completados
            deliverables = Deliverable.objects.filter(milestone__in=milestones)
            if deliverables.filter(done=False).exists():
                messages.error(request, "All deliverables must be completed before finishing the job.")
            else:
                projectContributor.finishJob = True
                projectContributor.save()
                messages.success(request, "The job has been marked as finished.")
            return redirect('clientDeliverable', pk=pk)

        # Aceptación o rechazo de entregables individuales
        deliverable_id = request.POST.get('deliverable_id')
        action = request.POST.get('action')
        deliverable = get_object_or_404(Deliverable, id=deliverable_id)


        if action == 'accept':
            # Verificamos que la evidencia esté cargada si es necesaria
            if deliverable.requiresEvidence and not deliverable.evidenceFile:
                deliverable.done = False
                deliverable.awaiting_approval = False
                deliverable.save()
                messages.error(request, f'The deliverable "{deliverable.name}" cannot be marked as completed without evidence.')
            else:
                deliverable.done = True
                deliverable.awaiting_approval = False
                deliverable.save()
                messages.success(request, f'The deliverable "{deliverable.name}" has been accepted and marked as completed.')
        elif action == 'reject':
            deliverable.awaiting_approval = False
            deliverable.done = False
            deliverable.approval_requested = False
            deliverable.save()
            messages.error(request, f'The deliverable "{deliverable.name}" was rejected.')

        return redirect('clientDeliverable', pk=pk)

    # Obtener todos los entregables del contribuidor del proyecto
    deliverables = Deliverable.objects.filter(milestone__in=milestones)

    # Verificar si todos los entregables están completados
    all_deliverables_completed = not deliverables.filter(done=False).exists()

    context = {
        'projectContributor': projectContributor,
        'deliverables': deliverables,
        'milestones': milestones,
        'all_deliverables_completed': all_deliverables_completed,
        'skills' : skills
    }

    return render(request, 'projects/client/clientDeliverable.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def listOfFreelancersProjectClient(request):
    return render(request, 'projects/client/listOfFreelancersProjectClient.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def applyProjectFreelancer(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)

    if projectContributor.approval_status == 'not_rejected':
        img = projectContributor.freelancer.profile_pic
        skills = projectContributor.project.skillExpertises.all()

        milestones = projectContributor.milestones.all()

        context = {
            'projectContributor': projectContributor,
            'skills' : skills,
            'img' : img,
            'skills' : skills,
            'milestones' : milestones,
        }
        return render(request, 'projects/client/applyProjectFreelancer.html', context)
    else:
        return redirect('notifications')

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def approveFreelancer(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)
    projectContributor.approval_status = "approved"
    projectContributor.save()
    return redirect('notifications')


@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def rejectFreelancer(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)
    projectContributor.approval_status = "rejected"
    projectContributor.save()
    return redirect('notifications')

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def approveProfileFreelancer(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)
    projectContributor.rejectionReason = "not_rejected"
    projectContributor.save()
    return redirect('notifications')


@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def rejectProfileFreelancer(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)
    projectContributor.rejectionReason = "profile_rejected"
    projectContributor.save()
    return redirect('notifications')

def apply_projects_freelancer_view(request, project_id):
    # Obtener el proyecto utilizando el ID proporcionado
    project = get_object_or_404(Project, id=project_id)

    # Puedes agregar lógica para obtener la solicitud del freelancer, si corresponde.
    # Suponiendo que tienes un modelo `ProjectContributor` o similar para las solicitudes:
    freelancer_request = project.contributors.filter(freelancer=request.user).first()

    context = {
        'project': project,
        'freelancer_request': freelancer_request,
    }
    
    return render(request, 'deliverablesProject.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def gateWay(request, project_contributor_id):
    project_contributor = get_object_or_404(ProjectContributor, id=project_contributor_id)

    # Solo permite el pago si `finishJob` es True
    if not project_contributor.finishJob:
        messages.error(request, 'Payment not allowed until the job is marked as complete.')
        return redirect('listFreelancer', pk=project_contributor.project.id)

    if request.method == 'POST':
        # Validar los datos recibidos en el formulario
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        card_name = request.POST.get('card_name')

        # Verificar que todos los campos estén completos
        if not all([card_number, expiry_date, cvv, card_name]):
            messages.error(request, 'All the fields are required.')
            return redirect('gateWay', project_contributor_id=project_contributor_id)

        # Si los campos están completos, redirige a confirmedPayment
        return redirect('confirmedPayment', project_contributor_id=project_contributor_id)

    context = {
        'freelancer': project_contributor.freelancer,
        'budget': project_contributor.budget,
        'project': project_contributor.project,
        'project_contributor_id': project_contributor_id,
    }
    return render(request, 'projects/client/gateWay.html', context)






@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def confirmedPayment(request, project_contributor_id):
    project_contributor = get_object_or_404(ProjectContributor, id=project_contributor_id)

    # Verifica que el trabajo esté finalizado
    if project_contributor.finishJob:
        # Crear una transacción con todos los detalles
        transaction = Transaction.objects.create(
            project_contributor=project_contributor,
            client=project_contributor.project.client,
            freelancer=project_contributor.freelancer,
            project=project_contributor.project,
            amount=project_contributor.budget,
            status='completed',  # La transacción se marca como completada
        )
        
         # Marca el pago como completado
        project_contributor.payment_completed = True
        project_contributor.save()
        
        
        #CHIMBADA MIA PA LA LEGIBILIDAD DE LOS VALORES CON MUCHOS CEROS 
   #-----------------------------------------------------------------------
        budget = project_contributor.budget
        impuestos = budget * Decimal('0.1')
        total = budget * Decimal('1.1')
        
        budget_formateado = f"{budget:,.2f}".replace(",", ".")
        impuestos_formateado = f"{impuestos:,.2f}".replace(",", ".")
        total_formateado = f"{total:,.2f}".replace(",", ".")
   #-----------------------------------------------------------------------   
        #CHIMBADA MIA PA LA LEGIBILIDAD DE LOS VALORES CON MUCHOS CEROS 
        
            
        # Actualizar el saldo del freelancer
        freelancer = project_contributor.freelancer
        freelancer.balance += project_contributor.budget  
        freelancer.save() 
        
        # Pasar todos los valores al contexto
        context = {
            'freelancer': freelancer,
            'budget': budget_formateado,
            'impuestos': impuestos_formateado,
            'total': total_formateado,
            'project': project_contributor.project,
            'transaction': transaction,
            'project_contributor_id': project_contributor_id,
        }
        
        messages.success(request, f'Payment to {project_contributor.freelancer} was successful.')
        return render(request, 'projects/client/confirmedPayment.html', context)

    messages.error(request, 'Payment could not be completed.')
    return redirect('listFreelancer', pk=project_contributor.project.id)





@login_required
@allowed_users(allowed_roles=['client'])
def financial_control(request):
    try:
        client = request.user.client
    except AttributeError:
        return HttpResponse("Error: No tienes un cliente asignado.")
    
    # Transacciones asociadas al cliente, separadas por estado
    transactions = Transaction.objects.filter(client=client)
    completed_transactions = transactions.filter(status='completed')
    
    
    # Obtener el último pago realizado
    last_payment = completed_transactions.order_by('-transaction_date').first()
    last_payment_made = last_payment.amount if last_payment else 0
    
    # Proyectos vinculados al cliente
    projects = ProjectContributor.objects.filter(project__client=client).select_related('project')
 
    # Contar los proyectos activos (en progreso)
    active_projects_count = projects.filter( project_status ='PENDING').count()
    
    pendingPayments = projects.filter(payment_completed = False).aggregate(Sum('budget'))['budget__sum']
    
    total_invested = projects.filter(payment_completed = True).aggregate(Sum('budget'))['budget__sum']
    

    # Contexto para el template
    context = {
        'projects': projects,
        'completed_transactions': completed_transactions,
        'last_payment_made': last_payment_made,
        'active_projects_count': active_projects_count,
        'client': client,
        'pending_payments' : pendingPayments,
        'total_invested': total_invested
    }

    return render(request, 'projects/client/ClientFinancialControl.html', context)



#FREELANCER------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def browseProjects(request):
    freelancer = request.user.freelancer

    projects = Project.objects

    myFilter = BrowseProjectFilter(request.GET, queryset=projects)
    projects = myFilter.qs

    # Obtener el criterio de ordenamiento
    sort_by = request.GET.get('sort_by', '-datePosted')
    projects = projects.order_by(sort_by)

    # Limitar los resultados
    #projects = projects[:15]

    context = {
        'projects': projects,
        'myFilter': myFilter,
        'sort_by': sort_by
    }

    return render(request, 'projects/freelancer/browseProject.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def browseOwnProjects(request):
    freelancer = request.user.freelancer

    # Proyectos a los que el freelancer ha aplicado y que están aprobados y no pagados
    applied_projects = ProjectContributor.objects.filter(
        freelancer=freelancer,
        approval_status='approved',
        payment_completed=False
    ).values_list('project_id', flat=True)

    # Filtrar los proyectos en los que el freelancer está trabajando o ha aplicado
    projects = Project.objects.filter(id__in=applied_projects)

    myFilter = BrowseProjectFilter(request.GET, queryset=projects)
    projects = myFilter.qs

    # Obtener el criterio de ordenamiento
    sort_by = request.GET.get('sort_by', '-datePosted')
    projects = projects.order_by(sort_by)

    # Limitar los resultados
    #projects = projects[:15]

    context = {
        'projects': projects,
        'myFilter': myFilter,
        'sort_by': sort_by
    }

    return render(request, 'projects/freelancer/browseOwnProjects.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def informationProject(request, pk):
    freelancer = request.user.freelancer
    project = get_object_or_404(Project, id=pk)
    skills = project.skillExpertises.all()
    client = project.client
    img = client.profile_pic

    totalProjects = Project.objects.filter(client=client).count()
    if request.method == 'POST':
        
        projectContributors = ProjectContributor.objects.filter(
            project=project,
            freelancer=freelancer
        )

        rejection_threshold_date = timezone.now() - timedelta(days=7)
        recent_rejection = projectContributors.filter(
            is_send=True,
            rejectionReason='profile_rejected',
            created__gte=rejection_threshold_date
        ).exists()

        if recent_rejection:
            messages.error(request, "You cannot apply for this project because your profile was recently rejected.")
            return redirect('browseProject')

        elif projectContributors.filter(approval_status='approved').exists():
            messages.error(request, "You are already working on or have worked on this project.")
            return redirect('browseProject')
        elif projectContributors.filter(is_send=True, approval_status="pending").exists():
            messages.error(request, "You are already waiting for a response for this project.")
            return redirect('browseProject')
        else:
            # Si no hay ninguno con approval_status='approved', continúa con la lógica deseada
            projectContributor = projectContributors.order_by('-created').first()
            if projectContributor:
                if projectContributor.approval_status == 'rejected':
                    projectContributor = None
                elif projectContributor.version != project.version:
                    projectContributor.delete()
                    projectContributor = None
                

            if not projectContributor:
                projectContributor = ProjectContributor.objects.create(
                    title=project.title,
                    description = project.description,
                    requiredPosition = project.requiredPosition,
                    budget = project.budget,
                    daysDuration = project.daysDuration,
                    project = project,
                    freelancer = freelancer,
                    version = project.version,
                    complexity = project.complexity,
                    is_send = True
                )
            messages.success(request, "Your application has been sent successfully.")
            return redirect('browseProject')

    context = {
        'project': project,
        'skills' : skills,
        'img' : img,
        'totalProjects': totalProjects,
    }

    return render(request, 'projects/freelancer/informationProject.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def addDeliverablesProject(request, pk):
    projectContributor = ProjectContributor.objects.get(id=pk)
    if projectContributor.approval_status == "pending":
        client = projectContributor.project.client
        img = client.profile_pic
        totalProjects = Project.objects.filter(client=client).count()
        skills = projectContributor.project.skillExpertises.all()

        milestones = projectContributor.milestones.all()

        form = MilestoneForm()
        if request.htmx:
            form = MilestoneForm(request.POST)
            if form.is_valid():
                milestone = form.save(commit=False)
                milestone.projectContributor = projectContributor
                milestone.save()

                context = {
                    'milestone' : milestone,
                }
                return render(request, 'projects/freelancer/partials/milestone.html', context)


        context = {
            'projectContributor': projectContributor,
            'skills' : skills,
            'img' : img,
            'totalProjects': totalProjects,
            'skills' : skills,
            'form' : form,
            'milestones' : milestones,
        }
        return render(request, 'projects/freelancer/addDeliverablesProject.html', context)
    else: 
        messages.error(request, "You cannot send the proposal because it has already been sent.")
        return redirect('notifications')
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def addMilestoneDeliverable(request, pk):
    
    milestone = Milestone.objects.get(id=pk)
    totalProjects = Project.objects.filter(client=milestone.projectContributor.project.client).count()
    img = milestone.projectContributor.project.client.profile_pic


    form = DeliverableForm()

    if request.method == 'POST':
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.milestone = milestone
            deliverable.save()

            if 'save' in request.POST:
                return redirect('addDeliverablesProject', milestone.projectContributor.id)
            
            # Si el botón "Save and go to browseProjects" fue presionado
            elif 'save_add_another' in request.POST:
                return redirect('addMilestoneDeliverable', milestone.id)

            return redirect('addMilestoneDeliverable', milestone.id)

    context = {
        'milestone' : milestone,
        'form' : form,
        'totalProjects': totalProjects,
        'img' : img,
    } 

    return render(request, 'projects/freelancer/addMilestoneDeliverable.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def deleteMilestone(request, pk):
    milestone = get_object_or_404(Milestone, id=pk)
    
    if request.method == "POST":
        # Al eliminar el milestone, guarda el id del projectContributor para la redirección
        pk = milestone.projectContributor.id
        milestone.delete()
        messages.success(request, 'Milestone deleted successfully.')
        
        # Redirige a la vista addDeliverablesProject usando el id del projectContributor
        return redirect('addDeliverablesProject', pk)
    
    return redirect('addMilestoneDeliverable', milestone.id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def deleteDeliverable(request, pk):
    deliverable = get_object_or_404(Deliverable, id=pk)
    
    if request.method == "POST":
        # Al eliminar el milestone, guarda el id del projectContributor para la redirección
        pk = deliverable.milestone.id
        deliverable.delete()
        messages.success(request, 'Milestone deleted successfully.')
        
        # Redirige a la vista addDeliverablesProject usando el id del projectContributor
        return redirect('addMilestoneDeliverable', pk)
    
    return redirect('addMilestoneDeliverable', deliverable.milestone.id)

def sendRequest(request, pk):
    projectContributor = get_object_or_404(ProjectContributor, id=pk)
    
    # Verificar que existen al menos 2 milestones y que cada uno tenga al menos 1 deliverable
    milestones = projectContributor.milestones.annotate(deliverable_count=Count('deliverables'))
    if len(milestones) < 2 or any(milestone.deliverable_count < 1 for milestone in milestones):
        messages.error(request, "Each milestone must have at least one deliverable, and there must be at least two milestones.")
        return redirect('addDeliverablesProject', pk=pk)
    
    total_days = sum(deliverable.deadlineInDays for milestone in milestones for deliverable in milestone.deliverables.all())
    
    if total_days > projectContributor.daysDuration:
        messages.error(request, "The total number of days for the deliverables exceeds the duration of the project.")
        return redirect('addDeliverablesProject', pk=pk)

    if request.method == "POST":
        # Actualizamos el estado del projectContributor
        projectContributor.approval_status = 'not_rejected'
        projectContributor.save()
        messages.success(request, "Your request has been sent successfully.")
        return redirect('browseProject')

    return redirect('addDeliverablesProject', pk=pk)


@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def freelancerProject(request):
    freelancer = request.user.freelancer
    contributors = ProjectContributor.objects.filter(freelancer=freelancer)
    projects = Project.objects.filter(projectContributor__in=contributors).distinct()

    myFilter = ProjectFilter(request.GET, queryset=projects)
    projects = myFilter.qs

    sort_by = request.GET.get('sort_by', '-datePosted')
    projects = projects.order_by(sort_by)

    #projects = projects[:15]

    context = {
        'projects': projects,
        'myFilter': myFilter,
        'sort_by': sort_by
    }

    return render(request, 'projects/freelancer/freelancerProject.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def deliverablesProject(request, pk):
    milestone = Milestone.objects.get(id=pk)
    img = milestone.projectContributor.project.client.profile_pic
    project = get_object_or_404(Project, id=pk)
    projectContributor = ProjectContributor.objects.filter(
        project=project, 
        freelancer=request.user.freelancer
    ).first()
    milestones = projectContributor.milestones.all()
    
    if request.method == 'POST':
        deliverable_id = request.POST.get('deliverable_id')
        deliverable = get_object_or_404(Deliverable, id=deliverable_id)
        
        # Verificar si se debe cambiar el estado a 'done'
        if 'mark_as_completed' in request.POST and not deliverable.requiresEvidence:
            deliverable.done = True
            deliverable.save()
            messages.success(request, f'The deliverable "{deliverable.name}" has been marked as completed.')
        
        # Subir o eliminar archivo de evidencia
        elif 'evidenceFile' in request.FILES:
            deliverable.evidenceFile = request.FILES['evidenceFile']
            deliverable.save()
            messages.success(request, f'Evidence file for "{deliverable.name}" uploaded successfully.')

        elif 'deleteFile' in request.POST:
            if deliverable.evidenceFile:
                file_path = os.path.join(settings.MEDIA_ROOT, str(deliverable.evidenceFile))
                if os.path.exists(file_path):
                    os.remove(file_path)
                deliverable.evidenceFile = None
                deliverable.approval_requested = False 
                deliverable.save()
                messages.success(request, 'The file has been deleted successfully.')

                    

        # Solicitar aprobación del cliente
        elif 'deliverable_id' in request.POST:
            if deliverable.requiresEvidence and not deliverable.evidenceFile:
                messages.error(request, f'Evidence is required for "{deliverable.name}" to request completion approval.')
            else:
                deliverable.awaiting_approval = True
                deliverable.approval_requested = True
                deliverable.save()
                messages.success(request, f'Request for approval sent for "{deliverable.name}".')

                # Notificación al cliente
                notificate.send(
                    sender=request.user,
                    verb=f'The deliverable "{deliverable.name}" for the project "{project.title}" has requested client approval.',
                    level='info',
                    destinity=project.client.user
                )
                
        return redirect('deliverablesProject', pk=pk)

    deliverables = Deliverable.objects.filter(milestone__projectContributor=projectContributor)

    context = {
        'projectContributor': projectContributor,
        'deliverables': deliverables,
        'project': project,
        'milestones': milestones,
        'img' : img,
    }

    return render(request, 'projects/freelancer/deliverablesProject.html', context)




@login_required
@allowed_users(allowed_roles=['freelancer'])
def freelancerfinancialcontrol(request):
   # Obtener el freelancer actual
    freelancer = request.user.freelancer
    
    # Transacciones asociadas al freelancer, separadas por estado
    transactions = Transaction.objects.filter(freelancer=freelancer)
    completed_transactions = transactions.filter(status='completed')
    pending_transactions = transactions.filter(status='pending')
    
    # Calcular los montos de pagos recibidos y pendientes
    total_received = completed_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_pending = pending_transactions.aggregate(total=Sum('amount'))['total'] or 0
    
    # Obtener el último pago recibido
    last_payment = completed_transactions.order_by('-transaction_date').first()
    last_payment_received = last_payment.amount if last_payment else 0
    
    # Proyectos vinculados al freelancer
    projects = ProjectContributor.objects.filter(freelancer=freelancer,  payment_completed = False).select_related('project')

    # Contar los proyectos activos (en progreso)
    active_projects_count = projects.filter(project_status='IN_PROGRESS').count()

    # Contexto para el template
    context = {
        'projects': projects,
        'completed_transactions': completed_transactions,
        'total_pending': total_pending,
        'total_received': total_received,
        'balance': freelancer.balance,
        'last_payment_received': last_payment_received,
        'active_projects_count': active_projects_count,
        'freelancer': freelancer,
    }

    return render(request, 'projects/freelancer/FreelancerFinancialControl.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def add_deliverable(request, project_contributor_id):
    if request.method == 'POST':
        project_contributor = get_object_or_404(ProjectContributor, id=project_contributor_id)
        form = DeliverableForm(request.POST)
        if form.is_valid():
            deliverable = form.save(commit=False)
            deliverable.projectContributor = project_contributor
            deliverable.save()
            messages.success(request, 'Deliverable added successfully.')
        else:
            messages.error(request, 'Error adding deliverable. Please check the form.')
        return redirect('deliverablesProject', pk=project_contributor.project.id)
    return redirect('deliverablesProject', pk=project_contributor.project.id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def apply_for_job(request, project_contributor_id):
    if request.method == 'POST':
        project_contributor = get_object_or_404(ProjectContributor, id=project_contributor_id)
        project_contributor.is_approved = True
        project_contributor.save()
        messages.success(request, 'You have successfully applied for this job.')
        return redirect('browseProject')
    return redirect('browseProject')

