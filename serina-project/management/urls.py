from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^classroom/list/$", views.ClassroomListView.as_view(),
        name="classroom_listview"),
    url(
        r"^classroom/read/(?P<pk>[0-9]+)/$",
        views.ClassroomDetailView.as_view(),
        name="classroom_detailview"
    ),

    url(r"^course/list/$", views.CourseListView.as_view(),
        name="course_listview"),
    url(r"^course/read/(?P<pk>[0-9]+)/$", views.CourseDetailView.as_view(),
        name="course_detailview"),

    url(r"^degree/list/$", views.DegreeListView.as_view(),
        name="degree_listview"),
    url(r"^degree/read/(?P<pk>[0-9]+)/$", views.DegreeDetailView.as_view(),
        name="degree_detailview"),

    url(r"^degree/category/list/$", views.DegreeCategoryListView.as_view(),
        name="degreecategory_listview"),
    url(
        r"^degree/category/read/(?P<pk>[0-9]+)/$",
        views.DegreeCategoryDetailView.as_view(),
        name="degreecategory_detailview"
    ),

    url(r"^module/list/$", views.ModuleListView.as_view(),
        name="module_listview"),
    url(r"^module/read/(?P<pk>[0-9]+)/$", views.ModuleDetailView.as_view(),
        name="module_detailview"),
    url(r"^module/create/$", views.ModuleCreateView.as_view(),
        name="module_createview"),
    url(r"^module/update/(?P<pk>[0-9]+)/$", views.ModuleUpdateView.as_view(),
        name="module_updateview"),
    url(r"^module/delete/(?P<pk>[0-9]+)/$", views.ModuleDeleteView.as_view(),
        name="module_deleteview"),

    url(r"^module/level/list/$", views.ModuleLevelListView.as_view(),
        name="modulelevel_listview"),
    url(
        r"^module/level/read/(?P<pk>[0-9]+)/$",
        views.ModuleLevelDetailView.as_view(),
        name="modulelevel_detailview"
    ),
    url(r"^module/level/create/$", views.ModuleLevelCreateView.as_view(),
        name="modulelevel_createview"),
    url(
        r"^module/level/update/(?P<pk>[0-9]+)/$",
        views.ModuleLevelUpdateView.as_view(),
        name="modulelevel_updateview",
    ),
    url(
        r"^module/level/delete/(?P<pk>[0-9]+)/$",
        views.ModuleLevelDeleteView.as_view(),
        name="modulelevel_deleteview",
    ),
]
