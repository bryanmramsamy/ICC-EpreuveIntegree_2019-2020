from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include


urlpatterns = [
    url(r"^", include('management.urls')),
    url(r"^admin/", admin.site.urls),
    url(r"^registration/", include('registration.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = "SERINA Back-Office"
admin.site.site_title = "Administration"
admin.site.index_title = "Superintent application for Educational " \
                         "Resources, Inscriptions and Network Administration"
