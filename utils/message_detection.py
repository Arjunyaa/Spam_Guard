"""
Message detection utilities using the trained SVM model
"""
import joblib
import os
from typing import Tuple, Dict
from .preprocessing import highlight_suspicious_words, extract_urls_from_text, get_message_features


class MessageDetector:
    """Handles message spam detection using trained model"""
    
    def __init__(self, model_path: str = 'models/message_model.pkl', 
                 vectorizer_path: str = 'models/message_vectorizer.pkl'):
        """
        Initialize the detector with trained model
        
        Args:
            model_path: Path to trained model file
            vectorizer_path: Path to fitted vectorizer file
        """
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model and vectorizer"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
            else:
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            if os.path.exists(self.vectorizer_path):
                self.vectorizer = joblib.load(self.vectorizer_path)
            else:
                raise FileNotFoundError(f"Vectorizer file not found: {self.vectorizer_path}")
                
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict if a message is spam or not
        
        Args:
            text: Message text to classify
            
        Returns:
            Tuple of (prediction, confidence)
        """
        if not text or not text.strip():
            return 'UNKNOWN', 0.0
        
        try:
            # Transform text using vectorizer
            text_vectorized = self.vectorizer.transform([text])
            
            # Get prediction
            prediction = self.model.predict(text_vectorized)[0]
            
            # Get decision function scores for confidence
            # LinearSVC uses decision_function instead of predict_proba
            decision_score = self.model.decision_function(text_vectorized)[0]
            
            # Convert decision function to probability-like score
            # Using sigmoid function: 1 / (1 + exp(-x))
            import numpy as np
            confidence = 1 / (1 + np.exp(-decision_score))
            
            # Map prediction to label
            label = 'SPAM' if prediction == 1 else 'SAFE'
            
            # Ensure confidence is in correct direction
            if label == 'SAFE':
                confidence = 1 - confidence
            
            return label, float(confidence)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return 'ERROR', 0.0
    
    def analyze_message(self, text: str, message_type: str = 'message') -> Dict:
        """
        Complete message analysis with explanation
        
        Args:
            text: Message text
            message_type: Type of message ('email' or 'sms')
            
        Returns:
            Complete analysis dictionary
        """
        if not text or not text.strip():
            return {
                'prediction': 'UNKNOWN',
                'confidence': 0.0,
                'suspicious_words': [],
                'categories': {},
                'urls': [],
                'features': {},
                'explanation': 'No text provided'
            }
        
        # Get prediction
        prediction, confidence = self.predict(text)
        
        # Find suspicious words
        suspicious_words, categories = highlight_suspicious_words(text)
        
        # Extract URLs
        urls = extract_urls_from_text(text)
        
        # Get message features
        features = get_message_features(text)
        
        # Generate explanation
        explanation = self._generate_explanation(
            prediction, confidence, suspicious_words, 
            categories, urls, features
        )
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'suspicious_words': suspicious_words,
            'categories': categories,
            'urls': urls,
            'features': features,
            'explanation': explanation
        }
    
    def _generate_explanation(self, prediction: str, confidence: float, 
                            suspicious_words: list, categories: dict, 
                            urls: list, features: dict) -> str:
        """
        Generate human-readable explanation for the classification
        
        Args:
            prediction: Classification result
            confidence: Confidence score
            suspicious_words: List of suspicious words found
            categories: Dictionary of categories and their keywords
            urls: List of URLs found
            features: Message feature dictionary
            
        Returns:
            Explanation string
        """
        explanations = []
        
        if prediction == 'SPAM':
            explanations.append(f"🚨 This message was classified as SPAM with {confidence*100:.1f}% confidence.")
            
            # Reasons for spam classification
            reasons = []
            
            if suspicious_words:
                reasons.append(f"Contains {len(suspicious_words)} suspicious keywords")
            
            if categories:
                category_names = list(categories.keys())
                reasons.append(f"Matches spam patterns: {', '.join(category_names[:3])}")
            
            if features.get('url_count', 0) > 0:
                reasons.append(f"Contains {features['url_count']} URL(s)")
            
            if features.get('exclamation_count', 0) > 2:
                reasons.append("Excessive exclamation marks")
            
            if features.get('uppercase_ratio', 0) > 0.3:
                reasons.append("High proportion of UPPERCASE text")
            
            if reasons:
                explanations.append("\n**Why it was flagged:**")
                for reason in reasons:
                    explanations.append(f"• {reason}")
            
            explanations.append("\n**⚠️ Recommended action:** Do not respond, click links, or share personal information.")
        
        elif prediction == 'SAFE':
            explanations.append(f"✅ This message appears to be legitimate with {confidence*100:.1f}% confidence.")
            
            if suspicious_words:
                explanations.append(f"\n⚠️ Note: Found {len(suspicious_words)} words that sometimes appear in spam, but overall message pattern is safe.")
            
            if urls:
                explanations.append(f"\nℹ️ Contains {len(urls)} URL(s). Always verify links before clicking.")
        
        else:
            explanations.append("Unable to classify this message.")
        
        return '\n'.join(explanations)
    
    def batch_predict(self, texts: list) -> list:
        """
        Predict multiple messages at once
        
        Args:
            texts: List of message texts
            
        Returns:
            List of (text, prediction, confidence) tuples
        """
        results = []
        for text in texts:
            pred, conf = self.predict(text)
            results.append((text, pred, conf))
        return results
