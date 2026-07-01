"""
views.py — All Views (Page Logic) for the Analyzer App
========================================================

Each view function handles one page of the website.
Views connect URLs to templates, process data, and return HTML.

Views in this file:
    1. home         → Landing page (GET)
    2. analyze      → Form page + analysis processing (GET/POST)
    3. result       → Display analysis result (GET)
    4. dashboard    → Analytics dashboard (GET)
    5. dashboard_data → JSON API for Chart.js charts (GET)
"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count

from .forms import NewsInputForm
from .models import NewsAnalysis
from .analysis_engine import analyze_text, FAKE_KEYWORDS


# ============================================================================
# VIEW 1: HOME PAGE
# ============================================================================

def home(request):
    """
    Landing page — shows project overview and a call-to-action button.
    Also shows a quick stat of total analyses performed.
    """
    total_analyses = NewsAnalysis.objects.count()
    return render(request, 'analyzer/home.html', {
        'total_analyses': total_analyses,
    })


# ============================================================================
# VIEW 2: ANALYZE PAGE (Form + Processing)
# ============================================================================

def analyze(request):
    """
    Handles the analysis form.
    
    GET request  → Show empty form
    POST request → Process form data, run analysis, save to database, redirect to result
    """
    if request.method == 'POST':
        form = NewsInputForm(request.POST)
        
        if form.is_valid():
            # Step 1: Get cleaned data from form
            headline = form.cleaned_data['headline']
            article_text = form.cleaned_data.get('article_text', '')
            
            # Step 2: Run the analysis engine
            result = analyze_text(headline, article_text)
            
            # Step 3: Save result to database
            analysis = NewsAnalysis.objects.create(
                headline=headline,
                article_text=article_text,
                score=result['score'],
                result_label=result['label'],
                matched_keywords=json.dumps({
                    'fake': result['matched_fake'],
                    'reliable': result['matched_reliable'],
                    'emotional': result['matched_emotional'],
                }),
            )
            
            # Step 4: Redirect to result page
            return redirect('result', analysis_id=analysis.id)
    else:
        form = NewsInputForm()
    
    return render(request, 'analyzer/analyze.html', {'form': form})


# ============================================================================
# VIEW 3: RESULT PAGE
# ============================================================================

def result(request, analysis_id):
    """
    Shows the result of a specific analysis.
    
    Retrieves the analysis from database using its ID.
    Parses the matched keywords JSON for display.
    """
    # get_object_or_404: returns the object or shows 404 error if not found
    analysis = get_object_or_404(NewsAnalysis, id=analysis_id)
    
    # Parse the stored JSON string back to a Python dictionary
    try:
        matched = json.loads(analysis.matched_keywords)
    except json.JSONDecodeError:
        matched = {'fake': [], 'reliable': [], 'emotional': []}
    
    # Determine CSS class for color coding
    if analysis.result_label == 'Likely Real':
        result_class = 'result-real'
        result_icon = '✅'
    elif analysis.result_label == 'Suspicious':
        result_class = 'result-suspicious'
        result_icon = '⚠️'
    else:
        result_class = 'result-fake'
        result_icon = '❌'
    
    return render(request, 'analyzer/result.html', {
        'analysis': analysis,
        'matched': matched,
        'result_class': result_class,
        'result_icon': result_icon,
    })


# ============================================================================
# VIEW 4: DASHBOARD PAGE
# ============================================================================

def dashboard(request):
    """
    Analytics dashboard showing:
    - Summary statistics
    - Recent analyses table
    - Charts are loaded via JavaScript using the dashboard_data API
    """
    # Get all analyses
    analyses = NewsAnalysis.objects.all()
    total = analyses.count()
    
    # Count by category
    real_count = analyses.filter(result_label='Likely Real').count()
    suspicious_count = analyses.filter(result_label='Suspicious').count()
    fake_count = analyses.filter(result_label='Likely Fake').count()
    
    # Calculate percentages (avoid division by zero)
    real_pct = round((real_count / total * 100), 1) if total > 0 else 0
    suspicious_pct = round((suspicious_count / total * 100), 1) if total > 0 else 0
    fake_pct = round((fake_count / total * 100), 1) if total > 0 else 0
    
    # Get last 20 analyses for the table
    recent = analyses[:20]
    
    return render(request, 'analyzer/dashboard.html', {
        'total': total,
        'real_count': real_count,
        'suspicious_count': suspicious_count,
        'fake_count': fake_count,
        'real_pct': real_pct,
        'suspicious_pct': suspicious_pct,
        'fake_pct': fake_pct,
        'recent': recent,
    })


# ============================================================================
# VIEW 5: DASHBOARD DATA API (for Chart.js)
# ============================================================================

def dashboard_data(request):
    """
    Returns JSON data for the dashboard charts.
    
    Chart.js (running in the browser) calls this URL via JavaScript fetch(),
    receives JSON data, and renders the charts.
    
    Returns:
        - pie_data: counts for Real/Suspicious/Fake (for pie chart)
        - bar_data: counts of most common fake keywords (for bar chart)
    """
    analyses = NewsAnalysis.objects.all()
    
    # --- Pie Chart Data ---
    pie_data = {
        'labels': ['Likely Real', 'Suspicious', 'Likely Fake'],
        'counts': [
            analyses.filter(result_label='Likely Real').count(),
            analyses.filter(result_label='Suspicious').count(),
            analyses.filter(result_label='Likely Fake').count(),
        ],
    }
    
    # --- Bar Chart Data: Count how often each fake keyword appears ---
    keyword_counts = {}
    for analysis in analyses:
        try:
            matched = json.loads(analysis.matched_keywords)
            for kw in matched.get('fake', []):
                keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        except json.JSONDecodeError:
            continue
    
    # Sort by count (most common first) and take top 10
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    bar_data = {
        'labels': [kw[0] for kw in sorted_keywords],
        'counts': [kw[1] for kw in sorted_keywords],
    }
    
    return JsonResponse({
        'pie_data': pie_data,
        'bar_data': bar_data,
    })
