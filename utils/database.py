"""
SQLite database operations for detection history
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd


class DetectionDatabase:
    """Handles all database operations for detection history"""
    
    def __init__(self, db_path: str = 'detection_history.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create detections table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detection_type TEXT NOT NULL,
                content TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL,
                risk_score INTEGER,
                explanation TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create URL scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                reasons TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_detection(self, detection_type: str, content: str, prediction: str, 
                     confidence: float = None, risk_score: int = None, 
                     explanation: str = None) -> int:
        """
        Add a detection record
        
        Args:
            detection_type: 'email', 'sms', or 'url'
            content: The content that was analyzed (truncated for privacy)
            prediction: Classification result
            confidence: Confidence score (0-1)
            risk_score: Risk score for URLs (0-100)
            explanation: Explanation of the detection
            
        Returns:
            ID of inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Truncate content for privacy (max 500 chars)
        content_truncated = content[:500] if content else ''
        
        cursor.execute('''
            INSERT INTO detections (detection_type, content, prediction, confidence, 
                                   risk_score, explanation, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (detection_type, content_truncated, prediction, confidence, 
              risk_score, explanation, datetime.now()))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def add_url_scan(self, url: str, risk_level: str, risk_score: int, 
                     reasons: List[str]) -> int:
        """
        Add a URL scan record
        
        Args:
            url: The URL that was scanned
            risk_level: Risk classification
            risk_score: Risk score (0-100)
            reasons: List of reasons for the classification
            
        Returns:
            ID of inserted record
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        reasons_text = ' | '.join(reasons) if reasons else ''
        
        cursor.execute('''
            INSERT INTO url_scans (url, risk_level, risk_score, reasons, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (url, risk_level, risk_score, reasons_text, datetime.now()))
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return record_id
    
    def get_all_detections(self, limit: int = 100) -> List[Dict]:
        """
        Get all detection records
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of detection dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, detection_type, content, prediction, confidence, 
                   risk_score, explanation, timestamp
            FROM detections
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        columns = ['id', 'detection_type', 'content', 'prediction', 'confidence',
                  'risk_score', 'explanation', 'timestamp']
        
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_detections_by_type(self, detection_type: str, limit: int = 100) -> List[Dict]:
        """
        Get detections filtered by type
        
        Args:
            detection_type: Type to filter by
            limit: Maximum number of records
            
        Returns:
            List of detection dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, detection_type, content, prediction, confidence, 
                   risk_score, explanation, timestamp
            FROM detections
            WHERE detection_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (detection_type, limit))
        
        columns = ['id', 'detection_type', 'content', 'prediction', 'confidence',
                  'risk_score', 'explanation', 'timestamp']
        
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_detections_by_prediction(self, prediction: str, limit: int = 100) -> List[Dict]:
        """
        Get detections filtered by prediction result
        
        Args:
            prediction: Prediction to filter by
            limit: Maximum number of records
            
        Returns:
            List of detection dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, detection_type, content, prediction, confidence, 
                   risk_score, explanation, timestamp
            FROM detections
            WHERE prediction LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{prediction}%', limit))
        
        columns = ['id', 'detection_type', 'content', 'prediction', 'confidence',
                  'risk_score', 'explanation', 'timestamp']
        
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def search_detections(self, search_term: str, limit: int = 100) -> List[Dict]:
        """
        Search detections by content
        
        Args:
            search_term: Term to search for
            limit: Maximum number of records
            
        Returns:
            List of matching detection dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, detection_type, content, prediction, confidence, 
                   risk_score, explanation, timestamp
            FROM detections
            WHERE content LIKE ? OR explanation LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (f'%{search_term}%', f'%{search_term}%', limit))
        
        columns = ['id', 'detection_type', 'content', 'prediction', 'confidence',
                  'risk_score', 'explanation', 'timestamp']
        
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def delete_detection(self, detection_id: int) -> bool:
        """
        Delete a detection record
        
        Args:
            detection_id: ID of record to delete
            
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM detections WHERE id = ?', (detection_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
    
    def clear_all_history(self) -> bool:
        """
        Clear all detection history
        
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM detections')
            cursor.execute('DELETE FROM url_scans')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get overall statistics
        
        Returns:
            Dictionary of statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total detections
        cursor.execute('SELECT COUNT(*) FROM detections')
        total_detections = cursor.fetchone()[0]
        
        # Spam count
        cursor.execute('''
            SELECT COUNT(*) FROM detections 
            WHERE prediction LIKE '%spam%' OR prediction LIKE '%SPAM%'
        ''')
        spam_count = cursor.fetchone()[0]
        
        # Safe count
        cursor.execute('''
            SELECT COUNT(*) FROM detections 
            WHERE prediction LIKE '%safe%' OR prediction LIKE '%ham%' 
            OR prediction LIKE '%legitimate%'
        ''')
        safe_count = cursor.fetchone()[0]
        
        # URL scans
        cursor.execute('SELECT COUNT(*) FROM url_scans')
        url_scans = cursor.fetchone()[0]
        
        # Suspicious URLs
        cursor.execute('''
            SELECT COUNT(*) FROM url_scans 
            WHERE risk_level IN ('HIGH RISK', 'SUSPICIOUS')
        ''')
        suspicious_urls = cursor.fetchone()[0]
        
        # Detections by type
        cursor.execute('''
            SELECT detection_type, COUNT(*) as count 
            FROM detections 
            GROUP BY detection_type
        ''')
        by_type = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_detections': total_detections,
            'spam_count': spam_count,
            'safe_count': safe_count,
            'url_scans': url_scans,
            'suspicious_urls': suspicious_urls,
            'by_type': by_type
        }
    
    def get_recent_activity(self, days: int = 7) -> pd.DataFrame:
        """
        Get recent activity for charts
        
        Args:
            days: Number of days to look back
            
        Returns:
            DataFrame with daily counts
        """
        conn = sqlite3.connect(self.db_path)
        
        query = f'''
            SELECT DATE(timestamp) as date, 
                   COUNT(*) as count,
                   detection_type
            FROM detections
            WHERE timestamp >= datetime('now', '-{days} days')
            GROUP BY DATE(timestamp), detection_type
            ORDER BY date DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def export_to_csv(self, filepath: str) -> bool:
        """
        Export all detections to CSV
        
        Args:
            filepath: Path to save CSV file
            
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query('SELECT * FROM detections ORDER BY timestamp DESC', conn)
            conn.close()
            
            df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
