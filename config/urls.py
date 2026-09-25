"""
URL configuration for Joseph Ashirumah - Full-Stack Software Engineer Portfolio.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('projects/', include('projects.urls')),
    path('contact/', include('contact.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

# Admin custom header & title
admin.site.site_header = "Joseph Ashirumah Portfolio Admin"
admin.site.site_title = "Joseph Ashirumah Portfolio"
admin.site.index_title = "Portfolio Content Management System"
