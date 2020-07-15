from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^login/$", views.CustomLoginView.as_view(), name="login"),
]
