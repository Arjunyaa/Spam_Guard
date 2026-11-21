import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import joblib

# Load your local CSV file (Replace 'spam.csv' with your actual file name)
# encoding='latin-1' prevents character decoding errors common in text datasets
df = pd.read_csv('spam.csv', encoding='latin-1')

# Select only v1 and v2 columns and rename them for clarity
df = df[['v1', 'v2']]
df.columns = ['label', 'message']

# Convert labels ('ham'/'spam') to numeric values (0/1)
df['label_num'] = df.label.map({'ham': 0, 'spam': 1})

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label_num'], test_size=0.2, random_state=42)

# Vectorize text using TF-IDF with unigrams and bigrams
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), min_df=2)
X_train_vec = vectorizer.fit_transform(X_train)

# Train the LinearSVC model
model = LinearSVC(random_state=42)
model.fit(X_train_vec, y_train)

# Save the trained model and vectorizer
joblib.dump(model, 'spam_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Model trained using your local dataset and saved successfully!")