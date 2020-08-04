from django.conf.urls import url

from . import views


urlpatterns = [


    # Homepage

    url(
        r"^$",
        views.home,
        name="home",
    ),


    # Authentication

    url(
        r"^login/$",
        views.CustomLoginView.as_view(),
        name="login",
    ),
    url(
        r"^logout/$",
        views.customLogout,
        name="logout",
    ),
    url(
        r"^register/$",
        views.register,
        name="register",
    ),

    # Password change

    url(
        r"^password/change/$",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    url(
        r"^password/change/done/$",
        views.post_password_change_logout,
        name="password_change_done",
    ),

    # Password reset

    url(
        r"^password/reset/$",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    url(
        r"^password/reset/done/$",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    url(
        r"^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/" \
        r"(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    url(
        r"^password/reset/complete/$",
        views.post_password_change_logout,
        name="password_reset_complete",
    ),


    # Profile

    url(
        r"^profile/r/(?P<pk>[0-9]+)/$",
        views.UserProfileDetailView.as_view(),
        name="userprofile_detailview",
    ),
    url(
        r"^profile/u/(?P<pk>[0-9]+)/$",
        views.UserProfileUpdateView.as_view(),
        name="userprofile_updateview",
    ),


    # RegistrationReports

    # StudentRegistrationReport

    url(
        r"^report/student/l/",
        views.StudentRegistrationReportListView.as_view(),
        name="student_rr_listview",
    ),
    url(
        r"^report/student/r/(?P<pk>[0-9]+)/$",
        views.StudentRegistrationReportDetailView.as_view(),
        name="student_rr_detailview",
    ),
    url(
        r"^report/student/c/$",
        views.StudentRegistrationReportCreateView.as_view(),
        name="student_rr_createview",
    ),

    # ModuleRegistrationReport

    url(
        r"^report/module/l/$",
        views.ModuleRegistrationReportListView.as_view(),
        name="module_rr_listview",
    ),
    url(
        r"^report/module/r/(?P<pk>[0-9]+)/$",
        views.ModuleRegistrationReportDetailView.as_view(),
        name="module_rr_detailview",
    ),
    url(
        r"^report/module/c/$",
        views.ModuleRegistrationReportCreateView.as_view(),
        name="module_rr_createview",
    ),

    # DegreeRegistrationReport

    url(
        r"^report/degree/l/$",
        views.DegreeRegistrationReportListView.as_view(),
        name="degree_rr_listview"
    ),
    url(
        r"^report/degree/r/(?P<pk>[0-9]+)/$",
        views.DegreeRegistrationReportDetailView.as_view(),
        name="degree_rr_detailview"
    ),
    url(
        r"^report/degree/c/$",
        views.DegreeRegistrationReportCreateView.as_view(),
        name="degree_rr_createview"
    ),
]
