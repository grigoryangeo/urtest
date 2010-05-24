from django.contrib import admin
from bugtracker.models import Bug, Project

class BugAdmin(admin.ModelAdmin):
    pass

class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bug, BugAdmin)
admin.site.register(Project, ProjectAdmin)
