from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^login/$", views.CustomLoginView.as_view(), name="login"),
    url(r"^logout/$", views.customLogout, name="logout"),

    url(r"^password/change/$", views.CustomPasswordChangeView.as_view(),
        name="password_change"),
    url(r"^password/change/done/$", views.customPasswordChangeDone,
        name="password_change_done"),

    url(r"^password/reset/$", views.CustomPasswordResetView.as_view(),
        name="password_reset"),

    url(r"^password/reset/done/$", views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done"),


]
