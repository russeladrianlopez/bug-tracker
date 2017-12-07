from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Bug
from .forms import ProjectForm, BugForm


# Create your views here.

class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 1
    template_name = 'tracker/project_detail.html'
    context_object_name = 'project_buglist'

    def get_queryset(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        return Bug.objects.filter(project_name_id=project.id)

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        context['project'] = Project.objects.get(slug=self.kwargs['slug'])
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class CreateProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'tracker/project_new.html'

    # send the user back to the projects list
    def get_success_url(self):
        return reverse('tracker:projects')


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = '__all__'
    template_name = 'tracker/project_form.html'
    context_object_name = 'project'

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:detail',
                       kwargs={'slug': self.kwargs['slug']})

    def get_object(self):
        # Only get the Project record for the user making the request
        return Project.objects.get(slug=self.kwargs['slug'])


class BugView(DetailView):
    model = Bug
    template_name = 'tracker/bug/bug_detail.html'
    context_object_name = 'bug'


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'tracker/bug/bug_list_all.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(BugListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


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


class UpdateBugView(LoginRequiredMixin, UpdateView):
    model = Bug
    fields = '__all__'
    template_name = 'tracker/bug/bug_update.html'
    context_object_name = 'bug'

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:bugdetail',
                       kwargs={'slug': self.kwargs['slug'],
                               'pk': self.kwargs['pk']})

    def get_object(self):
        # Only get the Project record for the user making the request
        return Bug.objects.get(id=self.kwargs['pk'])
