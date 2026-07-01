"""
analysis_engine.py — The Core of the Fake News Analyzer
=========================================================

This is the MOST IMPORTANT file in the project.
It contains the rule-based scoring system that classifies news as:
  - "Likely Real"   (score 0-2)
  - "Suspicious"    (score 3-6)
  - "Likely Fake"   (score 7+)

HOW IT WORKS:
1. We define lists of keywords that indicate fake or reliable news
2. We scan the user's input text for these keywords
3. Each match adds or subtracts from a score
4. The final score determines the classification

This is NOT machine learning — it's a simple rule-based system.
"""
import re

# ============================================================================
# KEYWORD DEFINITIONS
# ============================================================================

# Fake indicator keywords — words commonly found in clickbait/fake news
# Each match adds +2 to the score
FAKE_KEYWORDS = [
    'shocking',
    'breaking',
    'unbelievable',
    'secret',
    '100% guaranteed',
    "you won't believe",
    'miracle',
    'cure all',
    'conspiracy',
    'cover up',
    'they don\'t want you to know',
    'exposed',
    'hoax',
    'banned',
    'censored',
]

# Reliable indicator keywords — words found in credible reporting
# Each match subtracts -2 from the score
RELIABLE_KEYWORDS = [
    'study',
    'research',
    'report',
    'journal',
    'official',
    'published',
    'according to',
    'experts say',
    'peer reviewed',
    'university',
    'scientists',
    'data shows',
]

# Emotional exaggeration patterns — sensational language
# Each match adds +1 to the score
EMOTIONAL_PATTERNS = [
    '!!!',
    '???',
    'EXPOSED',
    'URGENT',
    'MUST SEE',
    'OMG',
    'WOW',
    'INCREDIBLE',
    'DESTROYED',
    'SLAMMED',
    'OBLITERATED',
    'WAKE UP',
    'SHARE BEFORE DELETED',
]


# ============================================================================
# MAIN ANALYSIS FUNCTION
# ============================================================================

def analyze_text(headline, article_text=""):
    """
    Analyze a news headline and optional article text for fake news indicators.
    
    Parameters:
        headline (str): The news headline (required)
        article_text (str): Optional article body text
    
    Returns:
        dict: Contains score, label, matched keywords, and explanation
    
    How scoring works:
        - Each fake keyword found     → +2 points
        - Each emotional pattern found → +1 point
        - Each reliable keyword found  → -2 points
        - Minimum score is 0 (can't go negative)
    
    Classification:
        - Score 0-2  → "Likely Real"
        - Score 3-6  → "Suspicious"
        - Score 7+   → "Likely Fake"
    """
    
    # Combine headline and article text into one string for analysis
    # Convert to lowercase so matching is case-insensitive
    full_text = f"{headline} {article_text}".lower()
    
    # Keep the original text for emotional pattern matching (case-sensitive)
    original_text = f"{headline} {article_text}"
    
    # Initialize score
    score = 0
    
    # Track which keywords were found (for the explanation)
    matched_fake = []
    matched_reliable = []
    matched_emotional = []
    
    # --- Step 1: Check for FAKE keywords ---
    for keyword in FAKE_KEYWORDS:
        # Use regex \b for word boundaries to prevent matching "secretary" when checking for "secret"
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', full_text):
            score += 2  # Each fake keyword adds 2 points
            matched_fake.append(keyword)
    
    # --- Step 2: Check for EMOTIONAL patterns ---
    for pattern in EMOTIONAL_PATTERNS:
        # Check both lowercase and original (for things like "!!!" and "EXPOSED")
        if pattern.lower() in full_text or pattern in original_text:
            score += 1  # Each emotional pattern adds 1 point
            matched_emotional.append(pattern)
    
    # --- Step 3: Check for RELIABLE keywords ---
    for keyword in RELIABLE_KEYWORDS:
        # Use regex \b for word boundaries
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', full_text):
            score -= 2  # Each reliable keyword subtracts 2 points
            matched_reliable.append(keyword)
    
    # --- Step 4: Ensure score doesn't go below 0 ---
    score = max(0, score)
    
    # --- Step 5: Classify based on score ---
    if score <= 2:
        label = "Likely Real"
    elif score <= 6:
        label = "Suspicious"
    else:
        label = "Likely Fake"
    
    # --- Step 6: Build explanation ---
    explanation = _build_explanation(score, label, matched_fake, matched_reliable, matched_emotional)
    
    return {
        'score': score,
        'label': label,
        'matched_fake': matched_fake,
        'matched_reliable': matched_reliable,
        'matched_emotional': matched_emotional,
        'explanation': explanation,
    }


def _build_explanation(score, label, matched_fake, matched_reliable, matched_emotional):
    """
    Build a human-readable explanation of the analysis result.
    This is shown to the user so they understand WHY the classification was made.
    """
    parts = []
    
    parts.append(f"Total Score: {score} → Classification: {label}")
    parts.append("")
    
    if matched_fake:
        parts.append(f" Fake indicators found ({len(matched_fake)} keywords, +2 each):")
        for kw in matched_fake:
            parts.append(f"  • \"{kw}\"")
        parts.append("")
    
    if matched_emotional:
        parts.append(f" Emotional/sensational language found ({len(matched_emotional)} patterns, +1 each):")
        for pattern in matched_emotional:
            parts.append(f"  • \"{pattern}\"")
        parts.append("")
    
    if matched_reliable:
        parts.append(f" Reliable indicators found ({len(matched_reliable)} keywords, -2 each):")
        for kw in matched_reliable:
            parts.append(f"  • \"{kw}\"")
        parts.append("")
    
    if not matched_fake and not matched_emotional and not matched_reliable:
        parts.append("No specific indicators were detected in the text.")
        parts.append("The text appears neutral based on our keyword analysis.")
    
    return "\n".join(parts)
