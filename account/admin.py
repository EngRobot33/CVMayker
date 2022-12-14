from django.contrib import admin
from .models import *


class HumanResourcesAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',)


admin.site.register(HumanResources, HumanResourcesAdmin)


class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'get_skill', 'project')

    def get_skill(self, obj):
        """
        Get all skills of the job-seeker
        """
        return [skill.title for skill in obj.skills.all()]


admin.site.register(JobSeeker, JobSeekerAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Skill, SkillAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Project, ProjectAdmin)
