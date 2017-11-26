from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.ProjectListView.as_view(),
        name='projects'
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
]
