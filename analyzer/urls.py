"""
urls.py — URL Routing for the Analyzer App
=============================================

Maps browser URLs to view functions.
Each path() connects a URL pattern to a view.

Example: when user visits /analyze/, Django calls views.analyze()
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page — the landing page
    path('', views.home, name='home'),
    
    # Analyze page — form to enter news + processing
    path('analyze/', views.analyze, name='analyze'),
    
    # Result page — shows analysis result for a specific analysis
    # <int:analysis_id> captures the ID from the URL (e.g., /result/5/)
    path('result/<int:analysis_id>/', views.result, name='result'),
    
    # Dashboard — analytics page with charts and tables
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # API endpoint — returns JSON data for Chart.js
    path('api/dashboard-data/', views.dashboard_data, name='dashboard_data'),
]
