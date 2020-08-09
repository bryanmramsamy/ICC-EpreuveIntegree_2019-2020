from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r"^l/^(?P<pk>\d+)/$",
        views.StudentRatingListView.as_view(),
        name="rating_listview.html"
    ),
    url(
        r"^r/^(?P<pk>\d+)/$",
        views.StudentRatingDetailView.as_view(),
        name="rating_detailview.html"
    ),
    url(
        r"^c/$",
        views.StudentRatingCreateView.as_view(),
        name="rating_createview"
    ),
    url(
        r"^u/^(?P<pk>\d+)/$",
        views.StudentRatingUpdateView.as_view(),
        name="rating_updateview.html"
    ),
    url(
        r"^d/^(?P<pk>\d+)/$",
        views.StudentRatingDeleteView.as_view(),
        name="rating_deleteview.html"
    ),
]
