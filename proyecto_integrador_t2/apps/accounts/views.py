from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import Template, Context
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Freelancer, Client, Userk, FreelancerSkillExpertise
from .forms import SignUpFormFreelancer, SignUpFormClient, ClientForm, FreelancerForm
from .decorators import unauthenticated_user
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import allowed_users
from .forms import PortfolioForm
from .models import Portfolio, Experience, Rating
from apps.projects.models import ProjectContributor
from .forms import RatingForm, ResponseForm
from django.http import JsonResponse
from .models import City

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_freelancer:
            login(request, user)
            return redirect('dashboardFreelancer') #Home page
        elif user is not None and user.is_client:
            login(request, user)
            return redirect('dashboardClient') #Home page
        elif user is not None and user.is_admin:
            login(request, user)
            return redirect('browseProject') #Home page
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('landpage')


@unauthenticated_user
def freelancerRegister(request):
    
    form = SignUpFormFreelancer()

    if request.method == 'POST':
        form = SignUpFormFreelancer(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_freelancer = True
            user.save()
            
            Freelancer.objects.create(
                user = user,
                phoneNumber=form.cleaned_data.get('phoneNumber'),
                email=form.cleaned_data.get('email'),
                identification=form.cleaned_data.get('identification')
            )

            username = form.cleaned_data.get('username')
          
            messages.success(request, 'Account was created for '+ username)

            return redirect('login')
        else:
            messages.success(request, 'Form is not valid')
    
    context = {'form':form}
    return render(request, 'accounts/freelancerRegister.html', context)


@unauthenticated_user
def clientRegister(request):
    form = SignUpFormClient()

    if request.method == 'POST':
        form = SignUpFormClient (request.POST)
        print("Urmum")
        if form.is_valid():
            print("Es valido")
            user = form.save(commit=False)
            user.is_client = True
            user.save()
            Client.objects.create(
                user = user,
                phoneNumber=form.cleaned_data.get('phoneNumber'),
                taxId=form.cleaned_data.get('taxId'),
                companyName=form.cleaned_data.get('companyName'),
                typeOfCompany=form.cleaned_data.get('typeOfCompany'),
                businessVertical=form.cleaned_data.get('businessVertical'),
                country=form.cleaned_data.get('country'),  
                city=form.cleaned_data.get('city'),  
                address=form.cleaned_data.get('address')
            )
            print(f"Cliente creado: {Client}")
            username = form.cleaned_data.get('username')
        
            messages.success(request, 'Account was created for '+ username)

            return redirect('login')
        else:
            
            # Mostrar y registrar los errores del formulario
            print("Errores de validación del formulario:", form.errors)
            messages.error(request, form.errors)


    
    context = {'form':form}
    return render(request, 'accounts/clientRegister.html', context)

@unauthenticated_user
def landpage(request):

    context = {}
    return render(request, 'accounts/landpage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def client_profile(request):
    client = request.user.client  # Esto agarra la información del cliente
    form = ClientForm(instance=client)  # Esto muestra el formulario ya con los datos del cliente
    
    if request.method == 'POST':  # Si el cliente hace clic en "Actualizar"
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()  # Guarda los cambios
            return redirect('clientProfile')  # Vuelve a cargar la página
    
    return render(request, 'accounts/clientProfile.html', {'form': form})


from .forms import FreelancerForm, PortfolioForm, ExperienceForm

@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def freelancer_profile_settings(request):
    freelancer = request.user.freelancer
    portfolio_count = freelancer.portfolios.count()
    if request.method == 'POST':
        form = FreelancerForm(request.POST, request.FILES, instance=freelancer)
        portfolio_form = PortfolioForm(request.POST, request.FILES)
        experience_form = ExperienceForm(request.POST)

        new_skills = request.POST.get('new_skills', '').split(',')

        if form.is_valid():
            form.save()
            for skill_name in new_skills:
                skill_name = skill_name.strip()
                if skill_name:
                    skill, created = FreelancerSkillExpertise.objects.get_or_create(name=skill_name)
                    freelancer.skillExpertises.add(skill)
        else:
            print("Errores de validación del formulario:", form.errors)
    

        if portfolio_form.is_valid() and portfolio_count < 9:  # Limitar a 9 portafolios
            portfolio = portfolio_form.save(commit=False)
            portfolio.freelancer = freelancer
            portfolio.save()
            messages.success(request, 'Portfolio item added successfully.')

        if experience_form.is_valid():
            experience = experience_form.save(commit=False)
            experience.freelancer = freelancer
            experience.save()
            messages.success(request, 'Work experience added successfully.')

        return redirect('freelancerProfileSettings')  # Redirigir después de guardar

    else:
        form = FreelancerForm(instance=freelancer)
        portfolio_form = PortfolioForm()
        experience_form = ExperienceForm()

    portfolios = freelancer.portfolios.all()[:9]  # Limitar a 9 portafolios
    experiences = freelancer.experiences.all()  # Obtener todas las experiencias laborales
    context = {
        'form': form,
        'portfolio_form': portfolio_form,
        'experience_form': experience_form,
        'freelancer': freelancer,
        'portfolios': portfolios,
        'experiences': experiences,
    }
    return render(request, 'accounts/freelancerProfileSettings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['freelancer'])
def delete_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id, freelancer=request.user.freelancer)
    if request.method == 'POST':
        portfolio.delete()
        messages.success(request, 'Portfolio item deleted successfully.')
    return redirect('freelancerProfile', pk=request.user.freelancer.user_id)

@login_required(login_url='login')
def freelancer_profile(request, pk=None):
    show = False
    projectContributor = ProjectContributor.objects.all().first()

    # Caso cuando el freelancer accede a su propio perfil
    if request.user.is_authenticated and request.user.is_freelancer and (pk is None or pk == request.user.freelancer.user_id):
        freelancer = request.user.freelancer
    else:
        # Caso cuando un cliente o cualquier otro usuario accede al perfil de un freelancer específico
        freelancer = get_object_or_404(Freelancer, user_id=pk)
        
    rating_form = RatingForm()
    response_form = ResponseForm()
    
    if request.method == 'POST':
        if 'rating_form' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                # Verificar que el cliente ha pagado por el proyecto
                project_contributor = ProjectContributor.objects.filter(
                    project__client=request.user.client,
                    freelancer=freelancer,
                    payment_completed=True
                ).exists()
                if project_contributor:
                    rating = rating_form.save(commit=False)
                    rating.client = request.user.client
                    rating.freelancer = freelancer
                    rating.save()
                    return redirect('freelancerProfile', pk=freelancer.user_id)
                else:
                    messages.error(request, 'You can only rate a freelancer after completing a payment.')
        elif 'response_form' in request.POST:
            response_form = ResponseForm(request.POST)
            if response_form.is_valid():
                rating_id = request.POST.get('rating_id')
                rating = get_object_or_404(Rating, id=rating_id, freelancer=freelancer)
                rating.response = response_form.cleaned_data['response']
                rating.save()
                return redirect('freelancerProfile', pk=freelancer.user_id)

    ratings = freelancer.ratings.all()
    
    notify = False
    talkMessage = request.user.is_client
    context = {
        'freelancer': freelancer,
        'notify' : notify,
        'projectContributor' : projectContributor,
        'show' : show,
        'ratings': ratings,
        'rating_form': rating_form,
        'response_form': response_form,
        'talkMessage' : talkMessage
    }
    return render(request, 'accounts/freelancerProfile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['client'])
def fprofileRequest(request, pk, contributorId):
    show = True
    projectContributor = get_object_or_404(ProjectContributor, id=contributorId)
    if projectContributor.rejectionReason == "pending":
        # Caso cuando el freelancer accede a su propio perfil
        if request.user.is_authenticated and request.user.is_freelancer and (pk is None or pk == request.user.freelancer.user_id):
            freelancer = request.user.freelancer
        else:
            # Caso cuando un cliente o cualquier otro usuario accede al perfil de un freelancer específico
            freelancer = get_object_or_404(Freelancer, user_id=pk)

        ratings = freelancer.ratings.all()
        notify = True
        talkMessage = request.user.is_client
        context = {
            'freelancer': freelancer,
            'notify' : notify,
            'projectContributor' : projectContributor,
            'show' : show,
            'ratings': ratings,
            'talkMessage' : talkMessage
        }
        return render(request, 'accounts/freelancerProfile.html', context)
    else:
        # Código para cuando el estado no es "pending"
        return redirect('notifications')
    