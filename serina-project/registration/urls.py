from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.home, name="home"),

    url(r"^login/$", views.CustomLoginView.as_view(), name="login"),
    url(r"^logout/$", views.customLogout, name="logout"),
    url(r"^register/$", views.register, name="register"),

    url(r"^password/change/$", views.CustomPasswordChangeView.as_view(),
        name="password_change"),
    url(r"^password/change/done/$", views.post_password_change_logout,
        name="password_change_done"),

    url(r"^password/reset/$", views.CustomPasswordResetView.as_view(),
        name="password_reset"),
    url(r"^password/reset/done/$", views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done"),
    url(r"^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm"),
    url(r"^password/reset/complete/$",
        views.post_password_change_logout,
        name="password_reset_complete"),
]
