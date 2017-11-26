from django.contrib import admin

from . import models

# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'tester', 'slug']
    fields = (
        'project_name',
        'tester',
        'start_date',
        'end_date',
        'staging_site',
        'production_site',
        'type_of_project',
    )


admin.site.register(models.Project, ProjectAdmin)
