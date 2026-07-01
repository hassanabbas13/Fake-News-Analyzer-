"""
forms.py — Django Form for User Input
=======================================

Django forms handle:
1. Rendering HTML form fields
2. Validating user input
3. Cleaning/sanitizing data

We have ONE form: NewsInputForm
"""

from django import forms


class NewsInputForm(forms.Form):
    """
    Form for users to enter news headline and optional article text.
    
    - headline: required text field (max 500 characters)
    - article_text: optional textarea for longer article content
    """
    
    headline = forms.CharField(
        max_length=500,
        required=False,
        label='News Headline',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter a news headline (optional)...',
            'id': 'headline-input',
        })
    )
    
    article_text = forms.CharField(
        label='Article Text',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Paste the full article text here...',
            'rows': 5,
            'id': 'article-input',
        })
    )
