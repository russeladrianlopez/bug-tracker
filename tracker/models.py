from django.db import models
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
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    staging_site = models.CharField(max_length=100, blank=True, null=True)
    production_site = models.CharField(max_length=100, blank=True, null=True)
    type_of_project = models.CharField(max_length=10, choices=TYPE_OF_PROJECT,
                                       default='Scrum')

    def __str__(self):
        return self.project_name
