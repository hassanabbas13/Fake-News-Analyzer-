"""
admin.py — Register models with Django Admin
==============================================

This makes our NewsAnalysis model visible and manageable
in the Django admin panel (accessible at /admin/).
"""

from django.contrib import admin
from .models import NewsAnalysis


@admin.register(NewsAnalysis)
class NewsAnalysisAdmin(admin.ModelAdmin):
    """Custom admin display for NewsAnalysis model."""
    list_display = ('headline', 'result_label', 'score', 'analyzed_at')
    list_filter = ('result_label',)
    search_fields = ('headline',)
    ordering = ('-analyzed_at',)
