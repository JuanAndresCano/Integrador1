from django.urls import path 
from . import views
from .views import apply_projects_freelancer_view

urlpatterns = [
    # client
    #SI
    path('createProject/', views.createProject, name="createProject"),
    #SI
    path('updateProject/<str:pk>/', views.updateProject, name="updateProject"),
    #SI
    path('clientProject/', views.clientProject, name='clientProject'),
    path('clientDeliverable/<str:pk>/', views.clientDeliverable, name="clientDeliverable"),
    path('listFreelancer/<str:pk>/', views.listFreelancer, name='listFreelancer'),
    path('listOfFreelancersProjectClient/', views.listOfFreelancersProjectClient, name='listOfFreelancersProjectClient'),
    path('clientFinancialControl/', views.financial_control, name='clientFinancialControl'),
    path('gateWay/<int:project_contributor_id>/', views.gateWay, name='gateWay'),
    path('confirmedPayment/<int:project_contributor_id>/', views.confirmedPayment, name='confirmedPayment'),
    
    
    path('applyProjectFreelancer/<str:pk>/', views.applyProjectFreelancer, name="applyProjectFreelancer"),
    path('approveFreelancer/<str:pk>/', views.approveFreelancer, name="approveFreelancer"),
    path('rejectFreelancer/<str:pk>/', views.rejectFreelancer, name="rejectFreelancer"),
    path('approveProfileFreelancer/<str:pk>/', views.approveProfileFreelancer, name="approveProfileFreelancer"),
    path('rejectProfileFreelancer/<str:pk>/', views.rejectProfileFreelancer, name="rejectProfileFreelancer"),

    #freelancer
    #SI
    path('browseProject/', views.browseProjects, name='browseProject'), 
    #SI
    path('browseOwnProjects/', views.browseOwnProjects, name='browseOwnProjects'),
    path('informationProject/<str:pk>/', views.informationProject, name='informationProject'),
    path('addDeliverablesProject/<str:pk>/', views.addDeliverablesProject, name='addDeliverablesProject'),
    path('addMilestoneDeliverable/<str:pk>/', views.addMilestoneDeliverable, name='addMilestoneDeliverable'),
    path('deleteMilestone/<str:pk>/', views.deleteMilestone, name='deleteMilestone'),
    path('deleteDeliverable/<str:pk>/', views.deleteDeliverable, name='deleteDeliverable'),
    
    path('sendRequest/<str:pk>/', views.sendRequest, name='sendRequest'),


    path('freelancerProject/', views.freelancerProject, name='freelancerProject'),
    path('deliverablesProject/<str:pk>/', views.deliverablesProject, name='deliverablesProject'),
    path('FreelancerFinancialControl/', views.freelancerfinancialcontrol, name='FreelancerFinancialControl'),

    #path('projects/<int:project_id>/approve/<int:freelancer_id>/', views.approve_freelancer_request, name='approve_freelancer'),
    #path('projects/<int:project_id>/reject/<int:freelancer_id>/', views.reject_freelancer_request, name='reject_freelancer'),

    # Cambiar a minúsculas y más coherente
    path('ApplyProject/<str:pk>/', views.deliverablesProject, name='ApplyProject'),

    
    # New URLs for adding deliverables and applying for jobs
    path('add-deliverable/<int:project_contributor_id>/', views.add_deliverable, name='add_deliverable'),
    path('apply-for-job/<int:project_contributor_id>/', views.apply_for_job, name='apply_for_job'),

    path('clientDeliverable/<int:pk>/', views.clientDeliverable, name='clientDeliverable'),



]
