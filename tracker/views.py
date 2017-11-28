from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Bug
from .forms import ProjectForm

# Create your views here.


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project


class CreateProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'tracker/project_new.html'

    # send the user back to the projects list
    def get_success_url(self):
        return reverse('tracker:projects')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project


class UpdateProjectView(LoginRequiredMixin, UpdateView):

    fields = '__all__'

    model = Project

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:detail',
                       kwargs={'slug': self.kwargs['slug']})

    def get_object(self):
        # Only get the Project record for the user making the request
        return Project.objects.get(slug=self.kwargs['slug'])


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'tracker/bug/bug_list_all.html'
