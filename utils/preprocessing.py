"""
Text preprocessing utilities for message analysis
"""
import re
import string
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and normalize text for analysis
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text


def extract_urls_from_text(text: str) -> List[str]:
    """
    Extract all URLs from text
    
    Args:
        text: Text containing potential URLs
        
    Returns:
        List of extracted URLs
    """
    if not text:
        return []
    
    # URL pattern matching http, https, www, and basic domain patterns
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    www_pattern = r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    urls = []
    
    # Find http/https URLs
    urls.extend(re.findall(url_pattern, text))
    
    # Find www URLs and add http://
    www_urls = re.findall(www_pattern, text)
    urls.extend(['http://' + url for url in www_urls])
    
    return list(set(urls))  # Remove duplicates


def get_suspicious_keywords() -> dict:
    """
    Get dictionary of suspicious keywords by category
    
    Returns:
        Dictionary mapping categories to keyword lists
    """
    return {
        'urgency': [
            'urgent', 'immediately', 'act now', 'limited time', 'expire', 
            'expires', 'hurry', 'only', 'today only', 'don\'t miss',
            'last chance', 'ending soon', 'time sensitive'
        ],
        'financial': [
            'free', 'cash', 'money', 'prize', 'winner', 'won', 'claim',
            'bonus', 'reward', 'gift card', 'refund', 'credit', '$$$',
            'earn', 'income', 'profit', 'investment', 'loan'
        ],
        'credential_phishing': [
            'verify', 'confirm', 'update', 'password', 'username', 'account',
            'suspended', 'locked', 'secure', 'login', 'signin', 'sign in',
            'security', 'authentication', 'validate', 'reactivate'
        ],
        'threats': [
            'suspended', 'blocked', 'restricted', 'violation', 'unauthorized',
            'illegal', 'action required', 'alert', 'warning', 'notice',
            'suspended', 'terminated', 'closed'
        ],
        'lottery_prize': [
            'congratulations', 'selected', 'winner', 'lottery', 'jackpot',
            'prize', 'award', 'chosen', 'lucky', 'draw', 'sweepstakes'
        ],
        'calls_to_action': [
            'click here', 'click now', 'call now', 'tap here', 'visit',
            'download', 'install', 'open', 'activate', 'redeem', 'claim now',
            'reply', 'respond', 'confirm now', 'verify now'
        ],
        'banking': [
            'bank', 'paypal', 'account', 'card', 'credit card', 'debit',
            'payment', 'transaction', 'transfer', 'wallet', 'banking'
        ],
        'otp_scam': [
            'otp', 'one time password', 'verification code', 'pin', 'code',
            'cvv', 'security code'
        ]
    }


def highlight_suspicious_words(text: str) -> tuple:
    """
    Find suspicious words in text and return them with categories
    
    Args:
        text: Text to analyze
        
    Returns:
        Tuple of (found_words, categories_dict)
    """
    if not text:
        return [], {}
    
    text_lower = text.lower()
    keywords_dict = get_suspicious_keywords()
    
    found_words = []
    categories_found = {}
    
    for category, keywords in keywords_dict.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                found_words.append(keyword)
                if category not in categories_found:
                    categories_found[category] = []
                categories_found[category].append(keyword)
    
    return list(set(found_words)), categories_found


def get_message_features(text: str) -> dict:
    """
    Extract statistical features from message text
    
    Args:
        text: Message text
        
    Returns:
        Dictionary of features
    """
    if not text:
        return {
            'length': 0,
            'word_count': 0,
            'uppercase_ratio': 0,
            'digit_count': 0,
            'special_char_count': 0,
            'url_count': 0,
            'has_phone': False,
            'has_email': False,
            'exclamation_count': 0
        }
    
    urls = extract_urls_from_text(text)
    
    # Phone number pattern
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\d{5,}\b'
    has_phone = bool(re.search(phone_pattern, text))
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    has_email = bool(re.search(email_pattern, text))
    
    uppercase_count = sum(1 for c in text if c.isupper())
    
    return {
        'length': len(text),
        'word_count': len(text.split()),
        'uppercase_ratio': uppercase_count / len(text) if len(text) > 0 else 0,
        'digit_count': sum(c.isdigit() for c in text),
        'special_char_count': sum(c in string.punctuation for c in text),
        'url_count': len(urls),
        'has_phone': has_phone,
        'has_email': has_email,
        'exclamation_count': text.count('!')
    }
