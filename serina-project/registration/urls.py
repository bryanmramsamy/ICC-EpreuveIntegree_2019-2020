from django.conf.urls import url

from . import views


urlpatterns = [
    # Homepage

    url(r"^$", views.home, name="home"),


    # Authentication

    url(r"^login/$", views.CustomLoginView.as_view(), name="login"),
    url(r"^logout/$", views.customLogout, name="logout"),
    url(r"^register/$", views.register, name="register"),

    # Password change

    url(r"^password/change/$", views.CustomPasswordChangeView.as_view(),
        name="password_change"),
    url(r"^password/change/done/$", views.post_password_change_logout,
        name="password_change_done"),

    # Password reset

    url(r"^password/reset/$", views.CustomPasswordResetView.as_view(),
        name="password_reset"),
    url(r"^password/reset/done/$", views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done"),
    url(
        r"^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/" \
        r"(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    url(
        r"^password/reset/complete/$",
        views.post_password_change_logout,
        name="password_reset_complete",
    ),


    # Profile

    url(r"^profile/(?P<pk>[0-9]+)/$", views.UserProfileDetailView.as_view(),
        name="userprofile_detailview"),
    


    # RegistrationReports

    url(
        r"^report/student/list/",
        views.StudentRegistrationReportListView.as_view(),
        name="student_rr_listview"
    ),
    url(
        r"^report/student/read/(?P<pk>[0-9]+)/$",
        views.StudentRegistrationReportDetailView.as_view(),
        name="student_rr_detailview"
    ),
    url(
        r"^report/student/create/$",
        views.StudentRegistrationReportCreateView.as_view(),
        name="student_rr_createview"
    ),

    url(
        r"^report/module/list/$",
        views.ModuleRegistrationReportListView.as_view(),
        name="module_rr_listview"
    ),
    url(
        r"^report/module/read/(?P<pk>[0-9]+)/$",
        views.ModuleRegistrationReportDetailView.as_view(),
        name="module_rr_detailview"
    ),
    url(
        r"^report/module/create/$",
        views.ModuleRegistrationReportCreateView.as_view(),
        name="module_rr_createview"
    ),
]
