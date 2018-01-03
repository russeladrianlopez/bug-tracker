from django.contrib import admin

from . import models


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = (
        'name',
        'project_type',
        'start_date',
        'end_date',
        'staging_site',
        'production_site',
    )


class BugReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'date_reported')
    # inlines = [BugClassificationInline, ReportedByInline, AssignedToInline]
    fields = (
        'project',
        'name',
        'bug_type',
        'bug_description',
        'steps_to_replicate',
        'actual_output',
        'expected_output',
        'date_reported',
    )


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Bug, BugReportAdmin)
