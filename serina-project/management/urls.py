from django.conf.urls import url

from . import views


urlpatterns = [


    # Classroom

    url(
        r"^classroom/l/$",
        views.ClassroomListView.as_view(),
        name="classroom_listview",
    ),
    url(
        r"^classroom/r/(?P<pk>[0-9]+)/$",
        views.ClassroomDetailView.as_view(),
        name="classroom_detailview",
    ),
    url(
        r"^classroom/c/$",
        views.ClassroomCreateView.as_view(),
        name="classroom_createview",
    ),
    url(
        r"^classroom/u/(?P<pk>[0-9]+)/$",
        views.ClassroomUpdateView.as_view(),
        name="classroom_updateview",
    ),
    url(
        r"^classroom/d/(?P<pk>[0-9]+)/$",
        views.ClassroomDeleteView.as_view(),
        name="classroom_deleteview",
    ),


    # Course

    url(
        r"^course/l/$",
        views.CourseListView.as_view(),
        name="course_listview",
    ),
    url(
        r"^course/ls/$",
        views.StudentCourseListView.as_view(),
        name="student_course_listview",
    ),
    url(
        r"^course/r/(?P<pk>[0-9]+)/$",
        views.CourseDetailView.as_view(),
        name="course_detailview",
    ),
    url(
        r"^course/c/$",
        views.CourseCreateView.as_view(),
        name="course_createview",
    ),
    url(
        r"^course/u/(?P<pk>[0-9]+)/$",
        views.CourseUpdateView.as_view(),
        name="course_updateview",
    ),
    url(
        r"^course/d/(?P<pk>[0-9]+)/$",
        views.CourseDeleteView.as_view(),
        name="course_deleteview",
    ),


    # Degree

    url(
        r"^degree/l/$",
        views.DegreeListView.as_view(),
        name="degree_listview",
    ),
    url(
        r"^degree/r/(?P<pk>[0-9]+)/$",
        views.DegreeDetailView.as_view(),
        name="degree_detailview",
    ),
    url(
        r"^degree/c/$",
        views.DegreeCreateView.as_view(),
        name="degree_createview",
    ),
    url(
        r"^degree/u/(?P<pk>[0-9]+)/$",
        views.DegreeUpdateView.as_view(),
        name="degree_updateview",
    ),
    url(
        r"^degree/d/(?P<pk>[0-9]+)/$",
        views.DegreeDeleteView.as_view(),
        name="degree_deleteview",
    ),

    # DegreeCategory

    url(
        r"^degree/category/l/$",
        views.DegreeCategoryListView.as_view(),
        name="degreecategory_listview",
    ),
    url(
        r"^degree/category/r/(?P<pk>[0-9]+)/$",
        views.DegreeCategoryDetailView.as_view(),
        name="degreecategory_detailview",
    ),
    url(
        r"^degree/category/c/$",
        views.DegreeCategoryCreateView.as_view(),
        name="degreecategory_createview",
    ),
    url(
        r"^degree/category/u/(?P<pk>[0-9]+)/$",
        views.DegreeCategoryUpdateView.as_view(),
        name="degreecategory_updateview",
    ),
    url(
        r"^degree/category/d/(?P<pk>[0-9]+)/$",
        views.DegreeCategoryDeleteView.as_view(),
        name="degreecategory_deleteview",
    ),


    # Module

    url(
        r"^module/l/$",
        views.ModuleListView.as_view(),
        name="module_listview",
    ),
    url(
        r"^module/r/(?P<pk>[0-9]+)/$",
        views.ModuleDetailView.as_view(),
        name="module_detailview",
    ),
    url(
        r"^module/c/$",
        views.ModuleCreateView.as_view(),
        name="module_createview",
    ),
    url(
        r"^module/u/(?P<pk>[0-9]+)/$",
        views.ModuleUpdateView.as_view(),
        name="module_updateview",
    ),
    url(
        r"^module/d/(?P<pk>[0-9]+)/$",
        views.ModuleDeleteView.as_view(),
        name="module_deleteview",
    ),


    # ModuleCategory

    url(
        r"^module/level/l/$",
        views.ModuleLevelListView.as_view(),
        name="modulelevel_listview",
    ),
    url(
        r"^module/level/r/(?P<pk>[0-9]+)/$",
        views.ModuleLevelDetailView.as_view(),
        name="modulelevel_detailview",
    ),
    url(
        r"^module/level/c/$",
        views.ModuleLevelCreateView.as_view(),
        name="modulelevel_createview",
    ),
    url(
        r"^module/level/u/(?P<pk>[0-9]+)/$",
        views.ModuleLevelUpdateView.as_view(),
        name="modulelevel_updateview",
    ),
    url(
        r"^module/level/d/(?P<pk>[0-9]+)/$",
        views.ModuleLevelDeleteView.as_view(),
        name="modulelevel_deleteview",
    ),
]
