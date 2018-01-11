from django.contrib import admin

from . import models


# Register your models here.
class TeamInline(admin.TabularInline):
    model = models.Team
    verbose_name = "Team Member"
    verbose_name_plural = "Team"
    min_num = 1
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [TeamInline, ]
    list_display = ['name', 'project_type', 'slug']
    fields = (
        'name',
        'project_type',
        'start_date',
        'end_date',
        'staging_site',
        'production_site',
    )


class BugClassificationInline(admin.TabularInline):
    model = models.BugClassification
    max_num = 1
    can_delete = False


class ReportedByInline(admin.StackedInline):
    model = models.ReportedBy
    max_num = 1
    can_delete = False


class AssignedToInline(admin.StackedInline):
    model = models.AssignedTo
    max_num = 1
    can_delete = False


class BugReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'date_reported')
    inlines = [BugClassificationInline, ReportedByInline, AssignedToInline]
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
