"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/packages/', include('apps.packages.urls')),
    path('api/bookings/', include('apps.bookings.urls')),
    path('api/forum/', include('apps.forum.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/ai/', include('apps.ai_services.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
