from django.conf.urls import url

from . import views


urlpatterns = [


    # General pages

    url(
        r"^$",
        views.home,
        name="home",
    ),
    url(  # TODO: Debug root
        r"^home$",
        views.home_old,
        name="home_old",
    ),
    url(
        r"^who_are_we/$",
        views.home,
        name="who_are_we"
    ),
    url(
        r"^contact/$",
        views.home,
        name="contact"
    ),
    url(
        r"^terms_and_conditions/$",
        views.terms_and_conditions,
        name="terms_and_conditions"
    ),
    url(
        r"^privacy_policy/$",
        views.privacy_policy,
        name="privacy_policy"
    ),
    url(
        r"^cookies_policy/$",
        views.cookies_policy,
        name="cookies_policy"
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
    url(
        r"^register/pursue/$",
        views.pursue_registration,
        name="pursue_registration"
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
        r"^password/reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$",
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
        r"^report/module/c/(?P<module_pk>\d+)/$",
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
        r"^report/degree/c/(?P<degree_pk>\d+)/$",
        views.DegreeRegistrationReportCreateView.as_view(),
        name="degree_rr_createview"
    ),


    # Back-Office functions

    url(
        r'^back_office/user_activation/(?P<user_pk>[0-9]+)/$',
        views.activate_deactivate_user,
        name='backoffice_user_activation'
    ),

    url(
        r'^back_office/module_validation/(?P<pk>[0-9]+)/$',
        views.module_validation,
        name='backoffice_module_validation'
    ),
    url(
        r'^back_office/module_deny/(?P<pk>[0-9]+)/$',
        views.module_deny,
        name='backoffice_module_deny'
    ),
    url(
        r'^back_office/module_score_submit/(?P<pk>[0-9]+)/$',
        views.module_score_submit,
        name='backoffice_module_score_submit'
    ),

    url(
        r'^back_office/degree_validation/(?P<pk>[0-9]+)/$',
        views.degree_validation,
        name='backoffice_degree_validation'
    ),
    url(
        r'^back_office/degree_deny/(?P<pk>[0-9]+)/$',
        views.degree_deny,
        name='backoffice_degree_deny'
    ),
    url(
        r'^back_office/degree_notes_submit/(?P<pk>[0-9]+)/$',
        views.degree_notes_submit,
        name='backoffice_degree_notes_submit'
    ),


    # Payment

    # Module Registration Report

    url(
        r"^payment/module/checkout/(?P<pk>\d+)/$",
        views.module_payment,
        name="module_payment"
    ),
    url(
        r'payment/module/done/$',
        views.module_payment_done,
        name='module_payment_done',
    ),
    url(
        r'payment/module/cancelled/$',
        views.module_payment_cancelled,
        name='module_payment_cancelled'
    ),

    # Degree Registration Report

    url(
        r"^payment/degree/checkout/(?P<pk>\d+)/$",
        views.degree_payment,
        name="degree_payment"
    ),
    url(
        r'payment/degree/done/$',
        views.degree_payment_done,
        name='degree_payment_done',
    ),
    url(
        r'payment/degree/cancelled/$',
        views.degree_payment_cancelled,
        name='degree_payment_cancelled'
    ),
]
