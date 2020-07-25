from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.home, name="home"),

    url(r"^module/list/$", views.ModuleListView.as_view(),
        name="module_listview"),

    url(r"^degree/list/$", views.DegreeListView.as_view(),
        name="degree_listview"),
]
