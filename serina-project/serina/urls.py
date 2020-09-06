from django.conf import settings
from django.conf.urls import (
  handler400,
  handler403,
  handler404,
  handler500,
  url,
)
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include

from registration import views

# i18n url patterns

urlpatterns = [
    url(r"^i18n/", include("django.conf.urls.i18n")),
]


# Project's apps urls patterns appended to i18n

urlpatterns += i18n_patterns(
    url(r"^", include('registration.urls')),
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include('api.urls')),
    url(r"^management/", include('management.urls')),
    url(r"^paypal/", include('paypal.standard.ipn.urls')),
    url(r"^rating/", include('rating.urls')),
    prefix_default_language=False,
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Handlers

handler400 = views.error_400
handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500


# Admin site settings

admin.site.site_header = "SERINA Back-Office"
admin.site.site_title = "Administration"
admin.site.index_title = "Superintent application for Educational " \
                         "Resources, Inscriptions and Network Administration"
admin.site.enable_nav_sidebar = False
