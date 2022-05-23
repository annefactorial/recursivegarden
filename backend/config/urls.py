import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path(settings.ADMIN_URL + "/", admin.site.urls),
    path('', include('backend.core.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
