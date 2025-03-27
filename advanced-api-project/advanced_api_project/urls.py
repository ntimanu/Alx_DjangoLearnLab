from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('api.urls')),
]
