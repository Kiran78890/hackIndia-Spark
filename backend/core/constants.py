# Scoring weights
SCORING_WEIGHTS = {
    'ai_analysis': 0.40,
    'source_verification': 0.35,
    'fact_check': 0.25
}

# Verdict ranges
VERDICT_RANGES = {
    'fake': (0, 40),
    'suspicious': (40, 70),
    'real': (70, 100)
}

# Verdicts
VERDICTS = {
    'fake': '🚨 FAKE NEWS',
    'suspicious': '⚠️ SUSPICIOUS',
    'real': '✅ LIKELY REAL'
}

# Colors
COLORS = {
    'fake': 'red',
    'suspicious': 'yellow',
    'real': 'green'
}

# Suspicious keywords
SUSPICIOUS_KEYWORDS = [
    'fake', 'hoax', 'conspiracy', 'allegedly', 'unverified', 
    'rumor', 'shocking', 'must see', 'breaking news', 
    'exclusive', 'you wont believe'
]

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'zh-cn': 'Chinese (Simplified)',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'te': 'Telugu',
    'mr': 'Marathi',
    'ta': 'Tamil',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
}