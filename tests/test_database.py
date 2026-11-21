"""
Tests for database functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import DetectionDatabase


def test_database_init():
    """Test database initialization"""
    print("Testing Database Initialization...")
    
    # Use test database
    db = DetectionDatabase('test_detection.db')
    
    print("✅ Database initialized successfully!\n")
    return db


def test_add_detection(db):
    """Test adding detection records"""
    print("Testing Add Detection...")
    
    record_id = db.add_detection(
        detection_type='email',
        content='Test spam message',
        prediction='SPAM',
        confidence=0.95,
        explanation='Test explanation'
    )
    
    print(f"Added record with ID: {record_id}")
    assert record_id > 0, "Should return valid record ID"
    
    print("✅ Add detection test passed!\n")


def test_add_url_scan(db):
    """Test adding URL scan records"""
    print("Testing Add URL Scan...")
    
    record_id = db.add_url_scan(
        url='http://test.example/page',
        risk_level='SUSPICIOUS',
        risk_score=45,
        reasons=['HTTP protocol', 'Suspicious keywords']
    )
    
    print(f"Added URL scan with ID: {record_id}")
    assert record_id > 0, "Should return valid record ID"
    
    print("✅ Add URL scan test passed!\n")


def test_get_all_detections(db):
    """Test retrieving all detections"""
    print("Testing Get All Detections...")
    
    detections = db.get_all_detections()
    
    print(f"Retrieved {len(detections)} detection(s)")
    assert isinstance(detections, list), "Should return list"
    
    if detections:
        print(f"First detection: {detections[0]['prediction']}")
    
    print("✅ Get all detections test passed!\n")


def test_get_statistics(db):
    """Test statistics generation"""
    print("Testing Statistics...")
    
    stats = db.get_statistics()
    
    print(f"Total detections: {stats['total_detections']}")
    print(f"Spam count: {stats['spam_count']}")
    print(f"Safe count: {stats['safe_count']}")
    print(f"URL scans: {stats['url_scans']}")
    print(f"Suspicious URLs: {stats['suspicious_urls']}")
    
    assert 'total_detections' in stats
    assert 'spam_count' in stats
    assert 'by_type' in stats
    
    print("✅ Statistics test passed!\n")


def test_search_detections(db):
    """Test search functionality"""
    print("Testing Search...")
    
    # Add a searchable record
    db.add_detection(
        detection_type='sms',
        content='Prize winner notification',
        prediction='SPAM',
        confidence=0.89
    )
    
    results = db.search_detections('prize')
    
    print(f"Search for 'prize' found {len(results)} result(s)")
    
    print("✅ Search test passed!\n")


def test_filter_by_type(db):
    """Test filtering by type"""
    print("Testing Filter by Type...")
    
    email_detections = db.get_detections_by_type('email')
    sms_detections = db.get_detections_by_type('sms')
    
    print(f"Email detections: {len(email_detections)}")
    print(f"SMS detections: {len(sms_detections)}")
    
    print("✅ Filter by type test passed!\n")


def test_filter_by_prediction(db):
    """Test filtering by prediction"""
    print("Testing Filter by Prediction...")
    
    spam_detections = db.get_detections_by_prediction('SPAM')
    safe_detections = db.get_detections_by_prediction('SAFE')
    
    print(f"SPAM detections: {len(spam_detections)}")
    print(f"SAFE detections: {len(safe_detections)}")
    
    print("✅ Filter by prediction test passed!\n")


def test_export_csv(db):
    """Test CSV export"""
    print("Testing CSV Export...")
    
    success = db.export_to_csv('test_export.csv')
    
    assert success == True, "Export should succeed"
    
    # Check if file exists
    assert os.path.exists('test_export.csv'), "CSV file should be created"
    
    print("✅ CSV export test passed!\n")


def test_delete_detection(db):
    """Test deleting a detection"""
    print("Testing Delete Detection...")
    
    # Add a record to delete
    record_id = db.add_detection(
        detection_type='test',
        content='Test delete',
        prediction='SPAM',
        confidence=0.5
    )
    
    # Delete it
    success = db.delete_detection(record_id)
    
    assert success == True, "Delete should succeed"
    
    print("✅ Delete detection test passed!\n")


def cleanup():
    """Clean up test files"""
    print("Cleaning up test files...")
    
    if os.path.exists('test_detection.db'):
        os.remove('test_detection.db')
        print("  Removed test database")
    
    if os.path.exists('test_export.csv'):
        os.remove('test_export.csv')
        print("  Removed test CSV")
    
    print("✅ Cleanup complete!\n")


if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE TESTS")
    print("=" * 60)
    print()
    
    db = None
    
    try:
        db = test_database_init()
        test_add_detection(db)
        test_add_url_scan(db)
        test_get_all_detections(db)
        test_get_statistics(db)
        test_search_detections(db)
        test_filter_by_type(db)
        test_filter_by_prediction(db)
        test_export_csv(db)
        test_delete_detection(db)
        
        print("=" * 60)
        print("✅ ALL DATABASE TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()
