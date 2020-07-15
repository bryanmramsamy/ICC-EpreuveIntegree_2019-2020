from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^login/$", views.CustomLoginView.as_view(), name="login"),
    url(r"^logout/$", views.customLogout, name="logout"),

    url(r"^password/change/$", views.CustomPasswordChangeView.as_view(), name="password_change"),
    
]
