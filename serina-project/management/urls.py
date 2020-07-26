from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.home, name="home"),

    url(r"^module/list/$", views.ModuleListView.as_view(),
        name="module_listview"),
    url(r"^module/read/(?P<pk>[0-9]+)/$", views.ModuleDetailView.as_view(),
        name="module_detailview"),

    url(r"^degree/list/$", views.DegreeListView.as_view(),
        name="degree_listview"),
    url(r"^degree/read/(?P<pk>[0-9]+)/$", views.DegreeDetailView.as_view(),
        name="degree_detailview"),
]
