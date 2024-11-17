import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from apps.projects.models import Project
from apps.accounts.models import Client

@pytest.mark.django_db
def testCreateProject(client):
    # Crear un cliente
    user = User.objects.create_user(username='testuser', password='12345')
    client_profile = Client.objects.create(user=user)

    # Autenticación del usuario
    client.login(username='testuser', password='12345')

    # Datos del proyecto a crear
    project_data = {
        'name': 'Test Project',
        'description': 'This is a test project',
        'client': client_profile.id,
    }

    # Hacer una solicitud POST para crear el proyecto
    response = client.post(reverse('create_project'), project_data)

    # Verificar que se haya creado correctamente
    assert response.status_code == 302  # Redirige después de crear
    assert Project.objects.filter(name='Test Project').exists()