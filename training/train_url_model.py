"""
Train URL classification model using the suspicious_url_dataset.csv
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
import joblib
import os
import sys

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.url_analyzer import extract_url_features


def extract_url_text_features(url):
    """
    Extract text-based features from URL for TF-IDF
    Converts URL into a space-separated string of components
    """
    features = extract_url_features(url)
    
    if 'error' in features:
        return url
    
    # Create a text representation of the URL
    parts = []
    parts.append(features.get('scheme', ''))
    parts.append(features.get('hostname', ''))
    parts.append(features.get('path', '').replace('/', ' '))
    parts.append(' '.join(features.get('suspicious_keywords', [])))
    
    # Add indicator words based on features
    if features.get('is_ip_address'):
        parts.append('has_ip_address')
    if features.get('has_at_symbol'):
        parts.append('has_at_symbol')
    if features.get('is_shortener'):
        parts.append('url_shortener')
    if features.get('has_punycode'):
        parts.append('punycode')
    if features.get('is_http'):
        parts.append('http_protocol')
    
    return ' '.join(parts)


def train_url_model():
    """Train and evaluate URL classification model"""
    
    print("=" * 60)
    print("URL CLASSIFICATION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    dataset_path = 'dataset/suspicious_url_dataset.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset not found at {dataset_path}")
        return False
    
    print(f"\n📁 Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path)
    
    print(f"✓ Loaded {len(df)} URL samples")
    print(f"\nDataset columns: {list(df.columns)}")
    
    # Check label distribution
    print("\n📊 Label Distribution:")
    print(df['label'].value_counts())
    print(f"\nBenign: {len(df[df['label']=='benign'])} URLs")
    print(f"Suspicious: {len(df[df['label']=='suspicious'])} URLs")
    
    # Prepare features and labels
    print("\n🔧 Extracting URL features...")
    df['url_text'] = df['url'].apply(extract_url_text_features)
    
    X = df['url_text']
    y = df['label'].map({'benign': 0, 'suspicious': 1})
    
    # Split data
    print("\n✂️ Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Create TF-IDF vectorizer
    print("\n🔤 Creating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 3),  # Use 1-3 character n-grams
        analyzer='char',  # Character-level analysis for URLs
        min_df=1
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"✓ Feature matrix shape: {X_train_vec.shape}")
    
    # Train model
    print("\n🤖 Training LinearSVC model...")
    model = LinearSVC(random_state=42, max_iter=2000)
    model.fit(X_train_vec, y_train)
    print("✓ Model training complete!")
    
    # Make predictions
    print("\n📈 Evaluating model performance...")
    y_pred = model.predict(X_test_vec)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE METRICS")
    print("=" * 60)
    print(f"Accuracy:  {accuracy*100:.2f}%")
    print(f"Precision: {precision*100:.2f}%")
    print(f"Recall:    {recall*100:.2f}%")
    print(f"F1-Score:  {f1*100:.2f}%")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n📊 Confusion Matrix:")
    print("                Predicted")
    print("               Benign  Suspicious")
    print(f"Actual Benign     {cm[0][0]:3d}      {cm[0][1]:3d}")
    print(f"       Suspicious {cm[1][0]:3d}      {cm[1][1]:3d}")
    
    # Detailed classification report
    print("\n📋 Detailed Classification Report:")
    print(classification_report(y_test, y_pred, 
                               target_names=['Benign', 'Suspicious']))
    
    # Cross-validation
    print("\n🔄 Performing 5-fold cross-validation...")
    cv_scores = cross_val_score(model, X_train_vec, y_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV accuracy: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")
    
    # Save model and vectorizer
    print("\n💾 Saving model and vectorizer...")
    os.makedirs('models', exist_ok=True)
    
    model_path = 'models/url_model.pkl'
    vectorizer_path = 'models/url_vectorizer.pkl'
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"✓ Model saved to: {model_path}")
    print(f"✓ Vectorizer saved to: {vectorizer_path}")
    
    # Test with some examples
    print("\n" + "=" * 60)
    print("TESTING WITH SAMPLE URLs")
    print("=" * 60)
    
    test_urls = [
        "https://www.example.com/contact",
        "http://claim-free-prize.example/urgent",
        "https://secure-bank-login.example/confirm",
        "https://www.example.com/search?query=weather"
    ]
    
    for url in test_urls:
        url_text = extract_url_text_features(url)
        url_vec = vectorizer.transform([url_text])
        pred = model.predict(url_vec)[0]
        label = 'Benign' if pred == 0 else 'Suspicious'
        print(f"\n{url}")
        print(f"  → Prediction: {label}")
    
    # Important note about dataset size
    print("\n" + "=" * 60)
    print("⚠️ IMPORTANT NOTE ABOUT MODEL LIMITATIONS")
    print("=" * 60)
    print(f"""
This model was trained on {len(df)} URL samples, which is a relatively
small dataset for machine learning. While it can detect patterns from
the training data, it may not generalize well to all real-world URLs.

The model should be used in combination with:
1. Heuristic URL analysis (url_analyzer.py)
2. User awareness and caution
3. Regular model updates with more data

DO NOT rely solely on this model for security-critical decisions.
    """)
    
    print("\n✅ URL model training complete!")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    try:
        success = train_url_model()
        if success:
            print("\n🎉 Training successful!")
        else:
            print("\n❌ Training failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
