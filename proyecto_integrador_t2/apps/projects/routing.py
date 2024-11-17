from django.urls import path
from .consumers import *  # Asegúrate de importar tu nuevo consumer

websocket_urlpatterns = [
    path("ws/milestones/<project_contributor_id>", MilestoneConsumer.as_asgi()),
]
