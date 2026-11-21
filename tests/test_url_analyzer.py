"""
Tests for URL analysis functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.url_analyzer import extract_url_features, calculate_url_risk_score, analyze_url, classify_url_risk


def test_benign_url():
    """Test analysis of benign URL"""
    print("Testing Benign URL...")
    
    url = "https://www.example.com/contact"
    result = analyze_url(url)
    
    print(f"URL: {url}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}/100")
    
    assert result['risk_level'] in ['BENIGN', 'LOW RISK'], f"Unexpected risk level: {result['risk_level']}"
    assert result['risk_score'] < 40, f"Risk score too high for benign URL: {result['risk_score']}"
    
    print("✅ Benign URL test passed!\n")


def test_suspicious_url():
    """Test analysis of suspicious URL"""
    print("Testing Suspicious URL...")
    
    url = "http://claim-free-prize.example/urgent"
    result = analyze_url(url)
    
    print(f"URL: {url}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Reasons: {len(result['reasons'])}")
    
    assert result['risk_level'] in ['SUSPICIOUS', 'HIGH RISK'], f"Should be flagged as suspicious: {result['risk_level']}"
    assert result['risk_score'] >= 30, f"Risk score too low: {result['risk_score']}"
    
    print("✅ Suspicious URL test passed!\n")


def test_ip_address_url():
    """Test IP address detection"""
    print("Testing IP Address URL...")
    
    url = "http://192.168.1.1/login"
    features = extract_url_features(url)
    
    print(f"URL: {url}")
    print(f"Is IP Address: {features['is_ip_address']}")
    
    assert features['is_ip_address'] == True, "Should detect IP address"
    
    risk_score, reasons = calculate_url_risk_score(features)
    print(f"Risk Score: {risk_score}/100")
    
    assert risk_score >= 30, "IP address URLs should have high risk score"
    
    print("✅ IP address test passed!\n")


def test_http_vs_https():
    """Test protocol detection"""
    print("Testing Protocol Detection...")
    
    http_url = "http://example.com/page"
    https_url = "https://example.com/page"
    
    http_result = analyze_url(http_url)
    https_result = analyze_url(https_url)
    
    print(f"HTTP URL Risk: {http_result['risk_score']}/100")
    print(f"HTTPS URL Risk: {https_result['risk_score']}/100")
    
    # HTTP should have higher risk than HTTPS (all else being equal)
    # Note: This is a weak test as other factors matter more
    assert http_result['features']['is_http'] == True
    assert https_result['features']['is_https'] == True
    
    print("✅ Protocol detection test passed!\n")


def test_suspicious_keywords():
    """Test suspicious keyword detection"""
    print("Testing Suspicious Keywords...")
    
    url = "https://secure-bank-login-verify-account.example/confirm"
    features = extract_url_features(url)
    
    print(f"URL: {url}")
    print(f"Suspicious Keywords: {features['suspicious_keywords']}")
    print(f"Keyword Count: {features['keyword_count']}")
    
    assert features['keyword_count'] > 0, "Should detect suspicious keywords"
    assert any(kw in ['login', 'verify', 'account', 'confirm'] for kw in features['suspicious_keywords'])
    
    print("✅ Keyword detection test passed!\n")


def test_url_length():
    """Test URL length analysis"""
    print("Testing URL Length...")
    
    short_url = "https://example.com/"
    long_url = "https://example.com/" + "a" * 150
    
    short_features = extract_url_features(short_url)
    long_features = extract_url_features(long_url)
    
    print(f"Short URL length: {short_features['url_length']}")
    print(f"Long URL length: {long_features['url_length']}")
    
    assert short_features['url_length'] < 50
    assert long_features['url_length'] > 100
    
    print("✅ URL length test passed!\n")


def test_at_symbol():
    """Test @ symbol detection"""
    print("Testing @ Symbol Detection...")
    
    url = "http://example.com@evil.com/login"
    features = extract_url_features(url)
    
    print(f"URL: {url}")
    print(f"Has @ Symbol: {features['has_at_symbol']}")
    
    assert features['has_at_symbol'] == True, "Should detect @ symbol"
    
    risk_score, reasons = calculate_url_risk_score(features)
    print(f"Risk Score: {risk_score}/100")
    
    assert risk_score >= 20, "@ symbol should increase risk"
    
    print("✅ @ symbol test passed!\n")


def test_batch_analysis():
    """Test batch URL analysis"""
    print("Testing Batch Analysis...")
    
    from utils.url_analyzer import batch_analyze_urls
    
    urls = [
        "https://www.example.com/about",
        "http://free-prize.example/claim",
        "https://www.example.org/contact"
    ]
    
    results = batch_analyze_urls(urls)
    
    print(f"Analyzed {len(results)} URLs")
    
    assert len(results) == len(urls), "Should return result for each URL"
    
    for result in results:
        print(f"  {result['url'][:40]}... -> {result['risk_level']} ({result['risk_score']}/100)")
        assert 'risk_level' in result
        assert 'risk_score' in result
    
    print("✅ Batch analysis test passed!\n")


def test_risk_classification():
    """Test risk level classification"""
    print("Testing Risk Classification...")
    
    test_scores = [5, 20, 45, 75]
    expected = ['BENIGN', 'LOW RISK', 'SUSPICIOUS', 'HIGH RISK']
    
    for score, expected_level in zip(test_scores, expected):
        level = classify_url_risk(score)
        print(f"Score {score} -> {level}")
        assert level == expected_level, f"Score {score} should be {expected_level}, got {level}"
    
    print("✅ Risk classification test passed!\n")


def test_invalid_url():
    """Test invalid URL handling"""
    print("Testing Invalid URL...")
    
    invalid_url = "not-a-valid-url"
    result = analyze_url(invalid_url)
    
    print(f"Invalid URL: {invalid_url}")
    print(f"Risk Level: {result['risk_level']}")
    
    # Should handle gracefully
    assert 'risk_level' in result
    
    print("✅ Invalid URL test passed!\n")


if __name__ == '__main__':
    print("=" * 60)
    print("URL ANALYZER TESTS")
    print("=" * 60)
    print()
    
    try:
        test_benign_url()
        test_suspicious_url()
        test_ip_address_url()
        test_http_vs_https()
        test_suspicious_keywords()
        test_url_length()
        test_at_symbol()
        test_batch_analysis()
        test_risk_classification()
        test_invalid_url()
        
        print("=" * 60)
        print("✅ ALL URL ANALYZER TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
