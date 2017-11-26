from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project
from .forms import ProjectForm

# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    # These next two lines tell the view to index lookups by username
    slug_field = 'project_name'
    slug_url_kwarg = 'project_name'


