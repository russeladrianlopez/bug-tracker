from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
from bug_report_tool.users.models import User


# Create your models here.
@python_2_unicode_compatible
class Project(models.Model):
    TYPE_OF_PROJECT = (
        ('Kanban', 'Kanban'),
        ('Scrum', 'Scrum'),
    )
    project_name = models.CharField(max_length=100, blank=False)
    tester = models.ForeignKey(User)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    staging_site = models.URLField(max_length=100, blank=True, null=True)
    production_site = models.URLField(max_length=100, blank=True, null=True)
    type_of_project = models.CharField(max_length=10, choices=TYPE_OF_PROJECT,
                                       default='Scrum')
    slug = AutoSlugField(populate_from=['project_name', ])

    def __str__(self):
        return self.project_name


@python_2_unicode_compatible
class Bug(models.Model):
    BUG_TYPE = (
        ('UI', 'User Interface'),
        ('functional', 'Functional'),
        ('recurring', 'Recurring'),
    )
    project_name = models.ForeignKey(Project, related_name='project')
    name = models.CharField(max_length=100, blank=False)
    bug_description = models.TextField(blank=True)
    steps_to_replicate = models.TextField(blank=True)
    actual_output = models.TextField(blank=True)
    expected_output = models.TextField(blank=True)
    date_reported = models.DateTimeField(blank=True, null=True)
    bug_type = models.CharField(max_length=15, choices=BUG_TYPE,
                                default='functional')

    def __str__(self):
        return self.name
