"""
Train message spam detection model using the spam.csv dataset
This script recreates the existing model with the same parameters
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
import joblib
import os


def train_message_model():
    """Train and evaluate message spam detection model"""
    
    print("=" * 60)
    print("MESSAGE SPAM DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    dataset_path = 'dataset/spam.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Error: Dataset not found at {dataset_path}")
        return False
    
    print(f"\n📁 Loading dataset from: {dataset_path}")
    df = pd.read_csv(dataset_path, encoding='latin-1')
    
    # Select relevant columns
    df = df[['v1', 'v2']]
    df.columns = ['label', 'message']
    
    print(f"✓ Loaded {len(df)} messages")
    
    # Check label distribution
    print("\n📊 Label Distribution:")
    print(df['label'].value_counts())
    ham_count = len(df[df['label'] == 'ham'])
    spam_count = len(df[df['label'] == 'spam'])
    print(f"\nHam (Safe): {ham_count} messages")
    print(f"Spam: {spam_count} messages")
    print(f"Spam ratio: {spam_count/len(df)*100:.1f}%")
    
    # Convert labels to numeric
    df['label_num'] = df.label.map({'ham': 0, 'spam': 1})
    
    # Split data
    print("\n✂️ Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['message'], df['label_num'], 
        test_size=0.2, random_state=42, stratify=df['label_num']
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    
    # Create TF-IDF vectorizer
    print("\n🔤 Creating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),  # Unigrams and bigrams
        min_df=2
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}")
    print(f"✓ Feature matrix shape: {X_train_vec.shape}")
    
    # Train model
    print("\n🤖 Training LinearSVC model...")
    model = LinearSVC(random_state=42)
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
    print("               Ham     Spam")
    print(f"Actual Ham     {cm[0][0]:3d}      {cm[0][1]:3d}")
    print(f"       Spam    {cm[1][0]:3d}      {cm[1][1]:3d}")
    
    tn, fp, fn, tp = cm.ravel()
    print(f"\nTrue Negatives:  {tn} (Ham correctly identified)")
    print(f"False Positives: {fp} (Ham incorrectly marked as Spam)")
    print(f"False Negatives: {fn} (Spam incorrectly marked as Ham)")
    print(f"True Positives:  {tp} (Spam correctly identified)")
    
    # Detailed classification report
    print("\n📋 Detailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))
    
    # Save model and vectorizer
    print("\n💾 Saving model and vectorizer...")
    os.makedirs('models', exist_ok=True)
    
    model_path = 'models/message_model.pkl'
    vectorizer_path = 'models/message_vectorizer.pkl'
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"✓ Model saved to: {model_path}")
    print(f"✓ Vectorizer saved to: {vectorizer_path}")
    
    # Test with some examples
    print("\n" + "=" * 60)
    print("TESTING WITH SAMPLE MESSAGES")
    print("=" * 60)
    
    test_messages = [
        "WINNER!! You have won a $1000 prize! Click to claim NOW!",
        "Hi, your appointment is confirmed for tomorrow at 2 PM",
        "URGENT: Your account will be suspended. Verify immediately!",
        "Thanks for your email. I'll get back to you soon."
    ]
    
    for msg in test_messages:
        msg_vec = vectorizer.transform([msg])
        pred = model.predict(msg_vec)[0]
        label = 'Spam' if pred == 1 else 'Ham'
        print(f"\nMessage: {msg[:60]}...")
        print(f"  → Prediction: {label}")
    
    print("\n✅ Message model training complete!")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    try:
        success = train_message_model()
        if success:
            print("\n🎉 Training successful!")
        else:
            print("\n❌ Training failed!")
            exit(1)
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
