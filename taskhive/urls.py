from django.urls import path, include, re_path
from django.views.static import serve

from django.conf import settings

from core.admin import taskhive_admin

urlpatterns = [
    path("admin/", taskhive_admin.urls),
    path("", include("core.urls")),
]

handler404 = "core.views.error_404"
handler500 = "core.views.error_500"

# Serve uploaded media files — works in both DEBUG=True and DEBUG=False.
# Django's static() helper silently skips the route when DEBUG=False,
# so we use re_path + serve directly to guarantee media is always accessible.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
