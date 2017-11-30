from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ProjectListView.as_view(),
        name='projects'
    ),
    url(
        regex=r'^recent_bugs/$',
        view=views.BugListView.as_view(),
        name='buglist'
    ),
    url(
        regex=r'^create/$',
        view=views.CreateProjectView.as_view(),
        name='create'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/$',
        view=views.ProjectDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<slug>[\w.@+-]+)/update/$',
        view=views.UpdateProjectView.as_view(),
        name='update'
    ),
    url(
        regex=r'^(?P<project_name>[\w.@+-]+)/bug/add/$',
        view=views.BugReportView.as_view(),
        name='newbug'
    ),

]
