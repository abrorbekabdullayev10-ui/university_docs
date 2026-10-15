from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Universitet Hujjatlar Tizimi — ADMIN"
admin.site.site_title = "Admin Panel"
admin.index_title = "Boshqaruv markazi"

urlpatterns = [
    path('messages/', include('apps.messaging.urls')),
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('documents/', include('apps.documents.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)