from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r"l/$",
        views.StudentRatingListView.as_view(),
        name="rating_listview"
    ),
    url(
        r"r/(?P<pk>[0-9]+)/$",
        views.StudentRatingDetailView.as_view(),
        name="rating_detailview"
    ),
    url(
        r"c/$",
        views.StudentRatingCreateView.as_view(),
        name="rating_createview"
    ),
    url(
        r"u/(?P<pk>[0-9]+)/$",
        views.StudentRatingUpdateView.as_view(),
        name="rating_updateview"
    ),
    url(
        r"d/(?P<pk>[0-9]+)/$",
        views.StudentRatingDeleteView.as_view(),
        name="rating_deleteview"
    ),

    # Actions

    url(
        r"v/(?P<pk>[0-9]+)/$",
        views.change_visibility,
        name="change_visibility"
    ),
]
