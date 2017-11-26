from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectForm

# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    # These next two lines tell the view to index lookups by username
    slug_field = 'project_name'
    slug_url_kwarg = 'project_name'


class CreateProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'tracker/project_new.html'

    # send the user back to the projects list
    # later update to send back to project details
    def get_success_url(self):
        return reverse('tracker:projects')
