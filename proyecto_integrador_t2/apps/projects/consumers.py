from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import Milestone, ProjectContributor
import json

class MilestoneConsumer(WebsocketConsumer):
    def connect(self):
        self.project_contributor_id = self.scope['url_route']['kwargs']['project_contributor_id']
        self.project_contributor = get_object_or_404(ProjectContributor, id=self.project_contributor_id)

        self.accept()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        milestone_name = text_data_json['name']

        milestone = Milestone.objects.create(
            name=milestone_name,
            projectContributor=self.project_contributor
        )
        
        context = {
            'milestone': milestone,
        }

        # Render HTML for milestone
        html = render_to_string("projects/freelancer/partials/milestone.html", context=context)
        self.send(text_data=html)
        
        
