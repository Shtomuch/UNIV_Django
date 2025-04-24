from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ci_cd_project2.urls')),  # ← змінити на назву твого додатку
    path('health/', lambda request: HttpResponse("OK")),
    path('files/', include('db_file_storage.urls')),
]

# для медіа-файлів
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
