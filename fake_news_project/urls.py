"""
URL configuration for the project.

This is the MAIN url file. It connects the browser URL to the correct view.
We include all URLs from the 'analyzer' app.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),       # Django admin panel
    path('', include('analyzer.urls')),     # All analyzer app URLs
]
