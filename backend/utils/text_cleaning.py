import re

def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\-]', '', text)
    
    return text.strip()

def extract_keywords(text: str, num_keywords: int = 5) -> list:
    """
    Extract keywords from text
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
    """
    words = text.lower().split()
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    return keywords[:num_keywords]

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text