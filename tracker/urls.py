from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ProjectListView.as_view(),
        name='project-list'
    ),
    url(
        regex=r'^recent_bugs/$',
        view=views.BugListView.as_view(),
        name='bug-list'
    ),
    url(
        regex=r'^create/$',
        view=views.ProjectCreateView.as_view(),
        name='project-create'
    ),
    url(
        regex=r'^(?P<project_name>[\w.@+-]+)/bug/add/$',
        view=views.BugCreateView.as_view(),
        name='bug-create'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/$',
        view=views.ProjectDetailView.as_view(),
        name='project-detail'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/(?P<pk>[\w-]+)/$',
        view=views.BugDetailView.as_view(),
        name='bug-detail'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/update/$',
        view=views.ProjectUpdateView.as_view(),
        name='project-update'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/(?P<pk>[\w-]+)/update/$',
        view=views.BugUpdateView.as_view(),
        name='bug-update'
    ),

]
