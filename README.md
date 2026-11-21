# 🛡️ SpamGuard AI

## Advanced AI-Powered Email, SMS & Phishing Protection System

---

## 📋 Project Overview

**SpamGuard AI** is a comprehensive, professional-grade security detection application that protects users from spam emails, scam SMS messages, and phishing URLs using advanced Machine Learning, Natural Language Processing, and heuristic analysis.

This upgraded project combines multiple detection systems into a unified, modern web application with:
- **Real-time spam detection** for emails and SMS
- **Intelligent URL security scanning** with risk scoring
- **Bulk processing** capabilities for CSV files
- **Analytics dashboard** with interactive charts
- **Detection history** with SQLite database
- **Modern glassmorphism UI** with responsive design

---

## ✨ Key Features

### 1. 📧 Email Spam Detection
- Analyze email subject lines and content
- Detect phishing and fraudulent attempts
- Extract and analyze embedded URLs
- Highlight suspicious keywords by category
- Provide confidence scores and explanations

### 2. 📱 SMS Scam Detection
- Identify lottery, prize, and OTP scams
- Detect financial fraud messages
- Flag urgency and threat tactics
- Extract and analyze URLs from messages
- Recognize common scam patterns

### 3. 🔗 URL Security Scanner
- Analyze URL structure and patterns without visiting them
- Detect IP-based phishing sites
- Identify URL shortener obfuscation
- Check for homograph and punycode attacks
- Calculate risk scores (0-100)
- Batch URL scanning

### 4. 📊 Bulk Detection
- Upload CSV files for batch processing
- Analyze multiple messages simultaneously
- Bulk URL scanning
- Export results to CSV

### 5. 📜 Detection History
- SQLite database for local storage
- Search and filter capabilities
- Export history to CSV
- Privacy-focused data handling

### 6. 📈 Analytics Dashboard
- Real-time statistics
- Interactive Plotly charts
- Threat trend analysis
- Protection impact metrics

### 7. 🎯 Model Performance
- Detailed model evaluation
- Confusion matrix visualization
- Compare multiple algorithms
- Performance metrics

---

## 🔧 Technology Stack

### Backend
- **Python 3.8+**
- **Scikit-learn** - Machine Learning
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations
- **SQLite** - Local database

### Frontend
- **Streamlit** - Web framework
- **Plotly** - Interactive visualizations
- **Custom CSS** - Glassmorphism design

### Machine Learning
- **TF-IDF** - Text vectorization
- **LinearSVC** - Primary classifier
- **NLP** - Text preprocessing
- **Heuristic Analysis** - URL pattern detection

---

## 📁 Project Structure

```
SpamGuard AI/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
│
├── models/                         # Trained ML models
│   ├── message_model.pkl           # Message spam classifier
│   ├── message_vectorizer.pkl      # TF-IDF vectorizer for messages
│   ├── url_model.pkl               # URL classifier (optional)
│   └── url_vectorizer.pkl          # URL vectorizer (optional)
│
├── pages/                          # Streamlit pages
│   ├── dashboard.py                # Main dashboard
│   ├── email_detection.py          # Email spam detection
│   ├── sms_detection.py            # SMS spam detection
│   ├── url_scanner.py              # URL security scanner
│   ├── bulk_detection.py           # Bulk processing
│   ├── history.py                  # Detection history
│   ├── analytics.py                # Analytics and charts
│   ├── model_performance.py        # Model evaluation
│   └── about.py                    # About page
│
├── utils/                          # Utility modules
│   ├── preprocessing.py            # Text preprocessing
│   ├── message_detection.py        # Message classifier
│   ├── url_analyzer.py             # URL analysis engine
│   ├── database.py                 # SQLite operations
│   └── ui_components.py            # UI styling
│
├── training/                       # Training scripts
│   ├── train_message_model.py      # Train message model
│   └── train_url_model.py          # Train URL model
│
├── dataset/                        # Datasets
│   ├── spam.csv                    # SMS spam dataset
│   └── suspicious_url_dataset.csv  # URL dataset
│
└── tests/                          # Unit tests
    ├── test_message_detection.py   # Message tests
    ├── test_url_analyzer.py        # URL tests
    ├── test_database.py            # Database tests
    └── run_all_tests.py            # Master test runner
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.8 or higher**
- **Windows CMD** (or PowerShell, Terminal on Mac/Linux)

### Step 1: Create Virtual Environment

Open Windows CMD and navigate to the project folder:

```cmd
cd "C:\Users\aarju\Downloads\ML Project"
python -m venv venv
```

### Step 2: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
```

### Step 4: Train the URL Model

```cmd
python training\train_url_model.py
```

This will:
- Load the URL dataset
- Train the URL classification model
- Save `url_model.pkl` and `url_vectorizer.pkl`
- Display performance metrics

**Note:** The message model (`message_model.pkl`) is already trained and included.

### Step 5: Run the Application

```cmd
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

---

## 💻 Usage Guide

### Email Detection
1. Navigate to **📧 Email Detection**
2. Enter email subject (optional) and message content
3. Click **🔍 Analyze Email**
4. View classification, confidence, and explanations
5. Check extracted URLs (if any)

### SMS Detection
1. Navigate to **📱 SMS Detection**
2. Paste SMS message text
3. Click **🔍 Analyze SMS**
4. View spam/safe classification
5. See suspicious keyword matches

### URL Scanner
1. Navigate to **🔗 URL Scanner**
2. Enter single URL or multiple URLs
3. Click **🔍 Scan URL**
4. View risk score (0-100) and risk level
5. Read detailed analysis and recommendations

### Bulk Processing
1. Navigate to **📊 Bulk Detection**
2. Upload CSV file (see template)
3. Click **🔍 Analyze All**
4. View summary and detailed results
5. Download results as CSV

### View History
1. Navigate to **📜 Detection History**
2. Search, filter by type or result
3. Export history to CSV
4. Delete individual records

---

## 🧪 Running Tests

Run all tests to verify everything works:

```cmd
python tests\run_all_tests.py
```

Individual test suites:

```cmd
python tests\test_message_detection.py
python tests\test_url_analyzer.py
python tests\test_database.py
```

---

## 🎓 For College Project / Viva

### Key Points to Remember

**1. What problem does this solve?**
- Protects users from spam, scams, and phishing attacks
- Automates detection using Machine Learning
- Provides explainable results

**2. Technologies Used**
- Python for backend
- Streamlit for UI
- Scikit-learn for ML
- TF-IDF for text features
- LinearSVC for classification

**3. How does it work?**
- Message Classification: TF-IDF → LinearSVC → Prediction
- URL Analysis: Pattern extraction → Heuristic rules → Risk scoring
- Database: SQLite for history storage

**4. Model Performance**
- Message Model: ~98% accuracy on test set
- Trained on 5,572 SMS messages
- Can detect common spam patterns

**5. Unique Features**
- Combined email, SMS, and URL detection
- Modern glassmorphism UI
- Real-time analytics
- Bulk processing
- Explainable AI (shows why messages are flagged)

### Viva Questions & Answers

**Q: Why LinearSVC instead of other algorithms?**
> LinearSVC is fast, efficient for high-dimensional text data, and proven effective for spam detection. It handles sparse TF-IDF matrices well and provides good accuracy.

**Q: How do you handle new spam patterns?**
> The model can be retrained periodically with new data. We also use heuristic rules for URL analysis that don't depend solely on training data.

**Q: What are the limitations?**
> Cannot detect image-based spam, language-specific (English), small URL dataset, requires periodic retraining, sophisticated attacks may bypass detection.

**Q: How is this different from existing spam filters?**
> Unified platform for email, SMS, and URLs; explainable results; local processing (privacy); modern UI; educational transparency.

**Q: How do you ensure privacy?**
> All processing is local, no data sent to external servers, SQLite database stored locally, users control their data.

---

## 📊 Model Details

### Message Classification Model
- **Algorithm**: LinearSVC
- **Features**: TF-IDF (unigrams + bigrams)
- **Training Data**: 5,572 SMS messages
- **Accuracy**: ~98%
- **Precision**: ~98%
- **Recall**: ~95%

### URL Analysis System
- **ML Model**: LinearSVC (character n-grams)
- **Training Data**: 60 labeled URLs
- **Heuristic Rules**: 12+ pattern checks
- **Risk Scoring**: 0-100 scale
- **Approach**: Hybrid (ML + heuristics)

---

## 🔒 Security & Privacy

- ✅ **Offline Analysis**: URLs analyzed without visiting
- ✅ **No Auto-Execution**: Links never opened automatically
- ✅ **Local Processing**: Everything runs on your machine
- ✅ **Privacy-First**: Data stored locally in SQLite
- ✅ **No Data Transmission**: Messages never sent externally
- ✅ **Transparent**: Clear explanations for all detections

**Important Notes:**
- HTTPS does NOT guarantee safety
- Use as one layer of defense
- Always verify unexpected communications
- Cannot detect all sophisticated attacks

---

## 📈 Future Enhancements

1. **Model Improvements**
   - Deep learning models (LSTM, BERT)
   - Ensemble methods
   - More training data
   - Multi-language support

2. **Features**
   - Real-time email client integration
   - Mobile app version
   - Browser extension
   - API endpoints

3. **Analysis**
   - Image-based spam detection
   - Sender reputation checking
   - Advanced NLP techniques
   - Behavioral analysis

---

## 🐛 Troubleshooting

**Issue: Module not found**
```cmd
Solution: Ensure virtual environment is activated and requirements installed
venv\Scripts\activate
pip install -r requirements.txt
```

**Issue: Model file not found**
```cmd
Solution: Train the models first
python training\train_url_model.py
```

**Issue: Streamlit won't start**
```cmd
Solution: Check if port 8501 is available
streamlit run app.py --server.port 8502
```

**Issue: Database errors**
```cmd
Solution: Delete detection_history.db and restart the app
```

---

## 👨‍💻 Project Information

**Project Name**: SpamGuard AI  
**Domain**: Machine Learning, Cybersecurity, NLP  
**Purpose**: College Project / Portfolio  
**Version**: 1.0.0  
**Python Version**: 3.8+  
**Framework**: Streamlit

---

## 🙏 Acknowledgments

- **UCI Machine Learning Repository** - SMS Spam Collection Dataset
- **Streamlit Team** - Web framework
- **Scikit-learn Contributors** - ML library
- **Plotly Team** - Visualization library

---

## ✅ Project Checklist

- [x] Message spam detection (Email & SMS)
- [x] URL security analysis
- [x] Bulk processing (CSV)
- [x] Detection history (SQLite)
- [x] Analytics dashboard
- [x] Model performance evaluation
- [x] Modern glassmorphism UI
- [x] Comprehensive testing
- [x] Complete documentation
- [x] Installation instructions
- [x] Viva preparation guide

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Run the test suite
4. Check Streamlit documentation

---

**Built with ❤️ using Python, Machine Learning & Streamlit**

**Good Luck with Your Project Presentation! 🎓🛡️**
