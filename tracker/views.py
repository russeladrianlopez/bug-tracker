from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Bug
from .forms import ProjectForm, BugForm

# Create your views here.


class ProjectBugMixin(LoginRequiredMixin, object):

    def get_project_bugs(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        return Bug.objects.filter(project_name_id=project.id)

    def get_context_data(self, **kwargs):
        context = super(ProjectBugMixin, self).get_context_data(**kwargs)
        context['bugs'] = self.get_project_bugs()
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project


class CreateProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'tracker/project_new.html'

    # send the user back to the projects list
    def get_success_url(self):
        return reverse('tracker:projects')


class ProjectDetailView(ProjectBugMixin, LoginRequiredMixin, DetailView):
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


class BugReportView(LoginRequiredMixin, CreateView):
    form_class = BugForm
    slug_field = 'project_name'
    slug_url_kwarg = 'project_name'
    template_name = 'tracker/bug/bug_new.html'

    def get_initial(self):
        project = Project.objects.get(slug=self.kwargs['project_name'])
        return {'project_name': project}

    # send the user back to the projects list
    def get_success_url(self):
        return reverse('tracker:detail',
                       kwargs={'slug': self.kwargs['project_name']})
