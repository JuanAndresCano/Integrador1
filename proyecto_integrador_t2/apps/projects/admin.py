from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ProjectSkillExpertise)
admin.site.register(ProjectComplexity)
admin.site.register(Project)
admin.site.register(Deliverable)
admin.site.register(Milestone)
admin.site.register(ProjectContributor)

