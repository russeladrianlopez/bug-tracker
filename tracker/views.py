from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import (TemplateView, ListView, CreateView,
                                  DetailView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Bug
from .forms import ProjectForm, BugForm


# General-Related Views
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['project_list'] = Project.objects.filter(
            tester=self.request.user.id).order_by("id")
        return context


# Project-Related Views

class ProjectDetailView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 5
    template_name = 'tracker/project/detail_page.html'
    context_object_name = 'project_buglist'

    def get_queryset(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        return Bug.objects.filter(project_name_id=project.id)

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        context['project'] = Project.objects.get(slug=self.kwargs['slug'])
        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tracker/project/list.html'
    paginate_by = 5

    def get_queryset(self):
        return Project.objects.filter(tester=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'tracker/project/create_form.html'
    success_url = reverse_lazy('tracker:projects')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = '__all__'
    template_name = 'tracker/project/update_form.html'
    context_object_name = 'project'

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:detail',
                       kwargs={'slug': self.kwargs['slug']})

    def get_object(self):
        # Only get the Project record for the user making the request
        return Project.objects.get(slug=self.kwargs['slug'])


# Bug-Related Views

class BugDetailView(LoginRequiredMixin, DetailView):
    model = Bug
    template_name = 'tracker/bug/detail_page.html'
    context_object_name = 'bug'


class BugListView(LoginRequiredMixin, ListView):
    model = Bug
    template_name = 'tracker/bug/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(BugListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class BugCreateView(LoginRequiredMixin, CreateView):
    form_class = BugForm
    slug_field = 'project_name'
    slug_url_kwarg = 'project_name'
    template_name = 'tracker/bug/create_form.html'

    def get_initial(self):
        project = Project.objects.get(slug=self.kwargs['project_name'])
        return {'project_name': project}

    # send the user back to the projects list
    def get_success_url(self):
        return reverse('tracker:detail',
                       kwargs={'slug': self.kwargs['project_name']})


class BugUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    fields = '__all__'
    template_name = 'tracker/bug/update_form.html'
    context_object_name = 'bug'

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:bugdetail',
                       kwargs={'slug': self.kwargs['slug'],
                               'pk': self.kwargs['pk']})

    def get_object(self):
        # Only get the Project record for the user making the request
        return Bug.objects.get(id=self.kwargs['pk'])
