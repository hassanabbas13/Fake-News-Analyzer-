"""
models.py — Database Models for the Analyzer App
==================================================

This file defines the database schema (structure).
Django automatically creates the database table from this model.

We have ONE model: NewsAnalysis
- It stores every analysis that a user performs
- This data is used for the analytics dashboard
"""

from django.db import models


class NewsAnalysis(models.Model):
    """
    Stores one news analysis result.
    
    Fields:
        headline       — The news headline entered by the user
        article_text   — Optional article body text
        score          — The computed score (0, 1, 2, 3, ... etc.)
        result_label   — "Likely Real", "Suspicious", or "Likely Fake"
        matched_keywords — JSON string storing which keywords were detected
        analyzed_at    — Timestamp of when the analysis was performed
    """
    
    headline = models.CharField(max_length=500, blank=True, default='')
    article_text = models.TextField()
    score = models.IntegerField()
    result_label = models.CharField(max_length=20)
    matched_keywords = models.TextField(default='{}')  # Stores JSON string
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Order by newest first
        ordering = ['-analyzed_at']
        verbose_name_plural = "News Analyses"
    
    def __str__(self):
        """String representation shown in Django admin"""
        return f"{self.headline[:50]} → {self.result_label} (Score: {self.score})"
