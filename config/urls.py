from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path(settings.DJANGO_ADMIN_URL + "/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', include('core.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
