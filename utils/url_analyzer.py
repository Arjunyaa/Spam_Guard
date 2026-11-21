"""
URL analysis and risk assessment utilities
"""
import re
import ipaddress
from urllib.parse import urlparse, parse_qs, unquote
from typing import Dict, List, Tuple


def extract_url_features(url: str) -> Dict:
    """
    Extract comprehensive features from a URL for analysis
    
    Args:
        url: URL string to analyze
        
    Returns:
        Dictionary of URL features
    """
    if not url or not isinstance(url, str):
        return {}
    
    try:
        # Parse the URL
        parsed = urlparse(url)
        
        # Basic components
        scheme = parsed.scheme.lower() if parsed.scheme else ''
        netloc = parsed.netloc.lower() if parsed.netloc else ''
        path = parsed.path if parsed.path else ''
        params = parsed.params if parsed.params else ''
        query = parsed.query if parsed.query else ''
        fragment = parsed.fragment if parsed.fragment else ''
        
        # Extract hostname (remove port if present)
        hostname = netloc.split(':')[0] if ':' in netloc else netloc
        
        # Check for IP address
        is_ip = False
        try:
            ipaddress.ip_address(hostname)
            is_ip = True
        except:
            pass
        
        # Count subdomains
        subdomain_count = hostname.count('.') if hostname else 0
        
        # Check for @ symbol (user info trick)
        has_at_symbol = '@' in netloc
        
        # URL length
        url_length = len(url)
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click']
        has_suspicious_tld = any(hostname.endswith(tld) for tld in suspicious_tlds)
        
        # Count hyphens in hostname
        hyphen_count = hostname.count('-')
        
        # Check for suspicious port
        port = None
        if ':' in netloc and not is_ip:
            try:
                port = int(netloc.split(':')[1])
            except:
                pass
        
        suspicious_ports = [8080, 8888, 8000, 3000, 4444, 5555]
        has_suspicious_port = port in suspicious_ports if port else False
        
        # Check for URL shorteners
        shortener_domains = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co', 'is.gd',
            'buff.ly', 'adf.ly', 'bit.do', 'tiny.cc'
        ]
        is_shortener = any(shortener in hostname for shortener in shortener_domains)
        
        # Check for punycode (IDN homograph attack)
        has_punycode = 'xn--' in hostname
        
        # Count dots in path
        path_dots = path.count('.')
        
        # Check for double slashes in path (除了开头)
        has_double_slash = '//' in path
        
        # Suspicious keywords in URL
        suspicious_keywords = [
            'login', 'signin', 'verify', 'account', 'update', 'confirm',
            'secure', 'banking', 'password', 'suspend', 'locked', 'urgent',
            'free', 'prize', 'winner', 'claim', 'reward', 'gift', 'bonus',
            'paypal', 'ebay', 'amazon', 'microsoft', 'apple', 'google',
            'netflix', 'facebook', 'instagram', 'whatsapp'
        ]
        
        url_lower = url.lower()
        matched_keywords = [kw for kw in suspicious_keywords if kw in url_lower]
        
        # Entropy calculation (measure of randomness)
        def calculate_entropy(text):
            if not text:
                return 0
            from collections import Counter
            import math
            counts = Counter(text)
            length = len(text)
            entropy = -sum((count/length) * math.log2(count/length) for count in counts.values())
            return entropy
        
        entropy = calculate_entropy(hostname)
        
        return {
            'url': url,
            'scheme': scheme,
            'hostname': hostname,
            'path': path,
            'query': query,
            'url_length': url_length,
            'is_https': scheme == 'https',
            'is_http': scheme == 'http',
            'is_ip_address': is_ip,
            'subdomain_count': subdomain_count,
            'has_at_symbol': has_at_symbol,
            'has_suspicious_tld': has_suspicious_tld,
            'hyphen_count': hyphen_count,
            'has_suspicious_port': has_suspicious_port,
            'port': port,
            'is_shortener': is_shortener,
            'has_punycode': has_punycode,
            'path_dots': path_dots,
            'has_double_slash': has_double_slash,
            'suspicious_keywords': matched_keywords,
            'keyword_count': len(matched_keywords),
            'entropy': entropy,
            'has_query': len(query) > 0,
            'query_length': len(query)
        }
    
    except Exception as e:
        return {'error': str(e), 'url': url}


def calculate_url_risk_score(features: Dict) -> Tuple[int, List[str]]:
    """
    Calculate risk score for URL based on extracted features
    
    Args:
        features: Dictionary of URL features
        
    Returns:
        Tuple of (risk_score 0-100, list of reasons)
    """
    if 'error' in features or not features:
        return 0, ['Unable to analyze URL']
    
    risk_score = 0
    reasons = []
    
    # HTTP instead of HTTPS (10 points)
    if features.get('is_http') and not features.get('is_https'):
        risk_score += 10
        reasons.append('❌ Uses HTTP instead of HTTPS')
    
    # IP address instead of domain (30 points - high risk)
    if features.get('is_ip_address'):
        risk_score += 30
        reasons.append('⚠️ Uses IP address instead of domain name')
    
    # Excessive URL length (15 points)
    if features.get('url_length', 0) > 100:
        risk_score += 15
        reasons.append(f"⚠️ Unusually long URL ({features['url_length']} characters)")
    
    # Too many subdomains (10 points)
    if features.get('subdomain_count', 0) > 3:
        risk_score += 10
        reasons.append(f"⚠️ Multiple subdomains ({features['subdomain_count']})")
    
    # @ symbol in URL (20 points)
    if features.get('has_at_symbol'):
        risk_score += 20
        reasons.append('⚠️ Contains @ symbol (URL obfuscation)')
    
    # Suspicious TLD (15 points)
    if features.get('has_suspicious_tld'):
        risk_score += 15
        reasons.append('⚠️ Suspicious top-level domain')
    
    # Excessive hyphens (8 points)
    if features.get('hyphen_count', 0) > 2:
        risk_score += 8
        reasons.append(f"⚠️ Multiple hyphens in domain ({features['hyphen_count']})")
    
    # Suspicious port (12 points)
    if features.get('has_suspicious_port'):
        risk_score += 12
        reasons.append(f"⚠️ Non-standard port ({features.get('port')})")
    
    # URL shortener (5 points - not always malicious)
    if features.get('is_shortener'):
        risk_score += 5
        reasons.append('ℹ️ URL shortening service (destination unknown)')
    
    # Punycode (25 points - homograph attack)
    if features.get('has_punycode'):
        risk_score += 25
        reasons.append('⚠️ Contains punycode (possible homograph attack)')
    
    # Suspicious keywords (5 points each, max 25)
    keyword_count = features.get('keyword_count', 0)
    if keyword_count > 0:
        keyword_score = min(keyword_count * 5, 25)
        risk_score += keyword_score
        keywords = ', '.join(features.get('suspicious_keywords', [])[:5])
        reasons.append(f"⚠️ Suspicious keywords: {keywords}")
    
    # High entropy (very random-looking) (10 points)
    if features.get('entropy', 0) > 4.5:
        risk_score += 10
        reasons.append('⚠️ Highly random-looking domain')
    
    # Double slash in path (5 points)
    if features.get('has_double_slash'):
        risk_score += 5
        reasons.append('⚠️ Unusual path structure')
    
    # Cap at 100
    risk_score = min(risk_score, 100)
    
    # Add positive indicators
    if features.get('is_https') and risk_score < 20:
        reasons.insert(0, '✓ Uses HTTPS encryption')
    
    if not features.get('is_ip_address') and not features.get('has_suspicious_tld') and risk_score < 15:
        reasons.insert(0, '✓ Legitimate domain structure')
    
    return risk_score, reasons


def classify_url_risk(risk_score: int) -> str:
    """
    Classify URL based on risk score
    
    Args:
        risk_score: Risk score from 0-100
        
    Returns:
        Risk classification string
    """
    if risk_score >= 60:
        return 'HIGH RISK'
    elif risk_score >= 30:
        return 'SUSPICIOUS'
    elif risk_score >= 15:
        return 'LOW RISK'
    else:
        return 'BENIGN'


def get_risk_color(risk_level: str) -> str:
    """
    Get color code for risk level
    
    Args:
        risk_level: Risk classification
        
    Returns:
        Color name for UI
    """
    colors = {
        'HIGH RISK': 'red',
        'SUSPICIOUS': 'orange',
        'LOW RISK': 'yellow',
        'BENIGN': 'green',
        'UNKNOWN': 'gray'
    }
    return colors.get(risk_level, 'gray')


def analyze_url(url: str) -> Dict:
    """
    Complete URL analysis pipeline
    
    Args:
        url: URL to analyze
        
    Returns:
        Complete analysis dictionary
    """
    # Extract features
    features = extract_url_features(url)
    
    if 'error' in features:
        return {
            'url': url,
            'risk_score': 0,
            'risk_level': 'UNKNOWN',
            'reasons': ['Invalid or malformed URL'],
            'features': features
        }
    
    # Calculate risk
    risk_score, reasons = calculate_url_risk_score(features)
    risk_level = classify_url_risk(risk_score)
    
    return {
        'url': url,
        'risk_score': risk_score,
        'risk_level': risk_level,
        'reasons': reasons,
        'features': features
    }


def batch_analyze_urls(urls: List[str]) -> List[Dict]:
    """
    Analyze multiple URLs
    
    Args:
        urls: List of URLs to analyze
        
    Returns:
        List of analysis results
    """
    return [analyze_url(url) for url in urls if url and url.strip()]
