from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
]

handler403 = 'dashboard.views.main.error_403'