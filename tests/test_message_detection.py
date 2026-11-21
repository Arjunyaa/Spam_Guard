"""
Tests for message detection functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.message_detection import MessageDetector


def test_spam_detection():
    """Test basic spam detection"""
    print("Testing Spam Detection...")
    
    detector = MessageDetector()
    
    # Test spam message
    spam_msg = "FREE entry to win a $1000 prize! Click here NOW to claim your reward!"
    prediction, confidence = detector.predict(spam_msg)
    
    print(f"Spam message: {spam_msg[:50]}...")
    print(f"Prediction: {prediction}")
    print(f"Confidence: {confidence:.2%}")
    
    assert prediction == 'SPAM', f"Expected SPAM, got {prediction}"
    assert confidence > 0.5, f"Confidence too low: {confidence}"
    
    print("✅ Spam detection test passed!\n")


def test_safe_message():
    """Test safe message detection"""
    print("Testing Safe Message Detection...")
    
    detector = MessageDetector()
    
    # Test safe message
    safe_msg = "Hi, your appointment is scheduled for tomorrow at 2 PM. See you then!"
    prediction, confidence = detector.predict(safe_msg)
    
    print(f"Safe message: {safe_msg[:50]}...")
    print(f"Prediction: {prediction}")
    print(f"Confidence: {confidence:.2%}")
    
    assert prediction == 'SAFE', f"Expected SAFE, got {prediction}"
    
    print("✅ Safe message test passed!\n")


def test_empty_message():
    """Test empty message handling"""
    print("Testing Empty Message Handling...")
    
    detector = MessageDetector()
    
    prediction, confidence = detector.predict("")
    
    print(f"Empty message prediction: {prediction}")
    assert prediction == 'UNKNOWN', f"Expected UNKNOWN, got {prediction}"
    
    print("✅ Empty message test passed!\n")


def test_analyze_message():
    """Test full message analysis"""
    print("Testing Full Message Analysis...")
    
    detector = MessageDetector()
    
    message = "WINNER! You've won $500. Visit http://claim-prize.example to claim NOW!"
    result = detector.analyze_message(message, 'sms')
    
    print(f"Message: {message[:50]}...")
    print(f"Prediction: {result['prediction']}")
    print(f"Suspicious words found: {len(result['suspicious_words'])}")
    print(f"URLs found: {len(result['urls'])}")
    
    assert result['prediction'] is not None
    assert 'explanation' in result
    assert isinstance(result['suspicious_words'], list)
    assert isinstance(result['urls'], list)
    
    print("✅ Full analysis test passed!\n")


def test_batch_prediction():
    """Test batch prediction"""
    print("Testing Batch Prediction...")
    
    detector = MessageDetector()
    
    messages = [
        "FREE gift card! Claim now!",
        "Your meeting is at 3 PM",
        "URGENT: Verify your account immediately"
    ]
    
    results = detector.batch_predict(messages)
    
    assert len(results) == len(messages)
    
    for msg, pred, conf in results:
        print(f"Message: {msg[:30]}... -> {pred} ({conf:.2%})")
    
    print("✅ Batch prediction test passed!\n")


if __name__ == '__main__':
    print("=" * 60)
    print("MESSAGE DETECTION TESTS")
    print("=" * 60)
    print()
    
    try:
        test_spam_detection()
        test_safe_message()
        test_empty_message()
        test_analyze_message()
        test_batch_prediction()
        
        print("=" * 60)
        print("✅ ALL MESSAGE DETECTION TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
