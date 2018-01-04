from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from bug_report_tool.users.models import User


# Create your models here.
@python_2_unicode_compatible
class Project(models.Model):
    TYPE_OF_PROJECT = (
        ('Kanban', 'Kanban'),
        ('Scrum', 'Scrum'),
    )
    name = models.CharField(_('Project Name'), max_length=100, blank=False)
    slug = AutoSlugField(populate_from=['name', ])
    project_type = models.CharField(_('Type of Project'), max_length=10,
                                    choices=TYPE_OF_PROJECT,
                                    default='Scrum')
    team = models.ManyToManyField(User, through='Team')
    start_date = models.DateTimeField(
        _('Starting Date'), blank=True, null=True)
    end_date = models.DateTimeField(_('Ending Date'), blank=True, null=True)
    staging_site = models.URLField(
        _('Staging URL'), max_length=100, blank=True, null=True)
    production_site = models.URLField(
        _('Production URL'), max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Team(models.Model):
    ROLES = (
        ('client', 'Client'),
        ('project_manager', 'Project Manager'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
    )
    project = models.ForeignKey(Project, related_name='team_project')
    member = models.ForeignKey(User, related_name="members")
    role = models.CharField(_('Team Role'), max_length=20, choices=ROLES,
                            default="developer")

    def __str__(self):
        return "Team " + self.project.name


@python_2_unicode_compatible
class Bug(models.Model):
    BUG_TYPE = (
        ('UI', 'User Interface'),
        ('functional', 'Functional'),
        ('recurring', 'Recurring'),
    )
    project = models.ForeignKey(Project, related_name='project')
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
