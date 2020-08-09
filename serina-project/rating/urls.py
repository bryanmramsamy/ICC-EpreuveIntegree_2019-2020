from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r"^c/$",
        views.StudentRatingCreateView.as_view(),
        name="rating_createview"
    )
]
