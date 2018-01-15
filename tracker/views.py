from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.views.generic import (TemplateView, ListView, CreateView,
                                  DetailView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Bug, User
from .forms import (ProjectForm, BugForm, ProjectTeamFormSet,
                    BugClassFormSet, BugAuthorFormSet)


# General-Related Views
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['project_list'] = Project.objects.filter(
            team__members__id=self.request.user.id).order_by("id")
        return context


# Project-Related Views

class ProjectDetailView(LoginRequiredMixin, ListView):
    model = Project
    paginate_by = 5
    template_name = 'tracker/project/detail_page.html'
    context_object_name = 'project_buglist'

    def get_queryset(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        return Bug.objects.filter(project_id=project.id)

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
        return Project.objects.filter(
            team__members__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'tracker/project/create_form.html'
    success_url = reverse_lazy('tracker:project-list')

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['team'] = ProjectTeamFormSet(self.request.POST)
        else:
            context['team'] = ProjectTeamFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        team = context['team']
        with transaction.atomic():
            self.object = form.save()

            if team.is_valid():
                team.instance = self.object
                team.save()
        return super(ProjectCreateView, self).form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'project_type', 'start_date', 'end_date',
              'staging_site', 'production_site']
    template_name = 'tracker/project/update_form.html'
    context_object_name = 'project'

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:project-detail',
                       kwargs={'slug': self.kwargs['slug']})

    def get_object(self):
        # Only get the Project record for the user making the request
        return Project.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)
        project = self.get_object()
        if self.request.POST:
            context['team'] = ProjectTeamFormSet(self.request.POST,
                                                 instance=project)
        else:
            context['team'] = ProjectTeamFormSet(instance=project)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        team = context['team']
        with transaction.atomic():
            self.object = form.save()

            if team.is_valid():
                team.instance = self.object
                team.save()
        return super(ProjectUpdateView, self).form_valid(form)


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
    template_name = 'tracker/bug/create_form.html'

    def get_initial(self):
        project = Project.objects.get(slug=self.kwargs['slug'])
        user = User.objects.get(id=self.request.user.id)
        return {'project': project, 'user': user}

    def get_context_data(self, **kwargs):
        context = super(BugCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['classification'] = BugClassFormSet(
                self.request.POST, prefix="classification")
            context['author'] = BugAuthorFormSet(
                self.request.POST, prefix="author")
        else:
            context['classification'] = BugClassFormSet(
                prefix="classification")
            context['author'] = BugAuthorFormSet(
                prefix="author",
                initial=[{'reported_by': self.get_initial()['user']}],
            )
            # Limit choices in reported_by fields
            # with only project team members
            for form in context['author']:
                form.fields['reported_by'].queryset = User.objects.filter(
                    project__slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        classification = context['classification']
        author = context['author']
        with transaction.atomic():
            self.object = form.save()

            if classification.is_valid():
                classification.instance = self.object
                classification.save()
            if author.is_valid():
                author.instance = self.object
                author.save()
        return super(BugCreateView, self).form_valid(form)

    # send the user back to the projects list
    def get_success_url(self):
        return reverse('tracker:project-detail',
                       kwargs={'slug': self.kwargs['project_name']})


class BugUpdateView(LoginRequiredMixin, UpdateView):
    model = Bug
    fields = '__all__'
    template_name = 'tracker/bug/update_form.html'
    context_object_name = 'bug'

    # send the user back to their own project page after a successful update
    def get_success_url(self):
        return reverse('tracker:bug-detail',
                       kwargs={'slug': self.kwargs['slug'],
                               'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(BugUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['classification'] = BugClassFormSet(self.request.POST)
        else:
            context['classification'] = BugClassFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        classification = context['classification']
        with transaction.atomic():
            self.object = form.save()

            if classification.is_valid():
                classification.instance = self.object
                classification.save()
        return super(BugUpdateView, self).form_valid(form)

    def get_object(self):
        # Only get the Project record for the user making the request
        return Bug.objects.get(id=self.kwargs['pk'])
