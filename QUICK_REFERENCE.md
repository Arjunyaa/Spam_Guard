# 🛡️ SpamGuard AI - Quick Reference Card

## 🚀 Quick Start (3 Steps)

```cmd
1. Double-click SETUP.bat        (First time only)
2. Double-click START_APP.bat    (Every time)
3. Open browser → http://localhost:8501
```

---

## 📝 Manual Commands

### First Time Setup
```cmd
cd "C:\Users\aarju\Downloads\ML Project"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python training\train_url_model.py
```

### Every Time You Run
```cmd
cd "C:\Users\aarju\Downloads\ML Project"
venv\Scripts\activate
streamlit run app.py
```

### Run Tests
```cmd
python tests\run_all_tests.py
```

---

## 📂 Key Files Location

```
Models:           models/*.pkl
Database:         detection_history.db
Dataset:          dataset/spam.csv
Training:         training/train_*.py
Tests:            tests/*.py
Main App:         app.py
```

---

## 🎯 Common Tasks

### Analyze an Email
1. Go to **📧 Email Detection**
2. Paste email content
3. Click **🔍 Analyze Email**

### Scan a URL
1. Go to **🔗 URL Scanner**
2. Enter URL
3. Click **🔍 Scan URL**

### Bulk Process
1. Go to **📊 Bulk Detection**
2. Upload CSV file
3. Click **🔍 Analyze All**

### View History
1. Go to **📜 Detection History**
2. Search/filter records
3. Export to CSV if needed

---

## 🔧 Troubleshooting Quick Fixes

### App won't start
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### Model not found
```cmd
python training\train_url_model.py
```

### Port already in use
```cmd
streamlit run app.py --server.port 8502
```

### Python not found
- Reinstall Python
- Check "Add to PATH" during installation

---

## 📊 Model Stats

**Message Model:**
- Accuracy: 98%
- Dataset: 5,572 messages
- Algorithm: LinearSVC + TF-IDF

**URL Model:**
- Accuracy: 83%
- Dataset: 60 URLs
- Method: ML + Heuristics

---

## 🎨 UI Navigation

```
🏠 Dashboard          → Statistics overview
📧 Email Detection    → Analyze emails
📱 SMS Detection      → Analyze SMS
🔗 URL Scanner        → Check URLs
📊 Bulk Detection     → Process CSV files
📜 Detection History  → View past scans
📈 Analytics          → Charts & insights
🎯 Model Performance  → Evaluation metrics
ℹ️ About             → Project info
```

---

## 💡 Example Test Cases

### Spam Email
```
Subject: WINNER!!
Body: You've won $1000! Click here NOW to claim!
Expected: SPAM (High confidence)
```

### Safe Email
```
Subject: Meeting Reminder
Body: Your appointment is tomorrow at 2 PM.
Expected: SAFE
```

### Suspicious URL
```
http://claim-free-prize.example/urgent
Expected: SUSPICIOUS or HIGH RISK
```

### Benign URL
```
https://www.example.com/contact
Expected: BENIGN or LOW RISK
```

---

## 📱 Viva Quick Answers

**Q: What does this project do?**
A: Detects spam in emails/SMS and analyzes URLs for phishing using Machine Learning.

**Q: What algorithm?**
A: LinearSVC with TF-IDF vectorization for text classification.

**Q: Why LinearSVC?**
A: Fast, efficient for text data, proven for spam detection, high accuracy.

**Q: How accurate?**
A: 98% for messages, combines ML with heuristic rules for URLs.

**Q: Technologies used?**
A: Python, Scikit-learn, Streamlit, Pandas, Plotly, SQLite.

**Q: Main features?**
A: Email/SMS detection, URL scanning, bulk processing, analytics, history.

**Q: How does URL analysis work?**
A: Checks protocol, domain structure, keywords, patterns - without visiting the URL.

**Q: Limitations?**
A: Can't detect all sophisticated attacks, needs periodic retraining, English only.

---

## 📦 Dependencies

```
streamlit>=1.28.0       # Web framework
pandas>=2.0.0           # Data manipulation
numpy>=1.24.0           # Numerical operations
scikit-learn>=1.3.0     # Machine Learning
joblib>=1.3.0           # Model persistence
plotly>=5.17.0          # Charts
python-dateutil>=2.8.2  # Date utilities
```

---

## 🔒 Security Notes

- ✅ Local processing (no cloud)
- ✅ URLs analyzed without visiting
- ✅ Privacy-first design
- ⚠️ HTTPS ≠ Safe
- ⚠️ Not 100% accurate
- ⚠️ Use as one layer of defense

---

## 📞 Need Help?

1. Check **README.md** for detailed docs
2. Check **INSTALLATION_GUIDE.md** for setup help
3. Check **PROJECT_SUMMARY.md** for overview
4. Run tests: `python tests\run_all_tests.py`
5. Check terminal for error messages

---

## ⚡ Performance Tips

- First load takes ~5 seconds
- Bulk processing: <500 rows recommended
- Clear history periodically
- Close unused browser tabs
- Use Chrome/Edge for best performance

---

## 🎓 Demo Flow (5 Minutes)

```
1. Show Dashboard (30s)
   → Explain statistics

2. Email Detection (1m)
   → Paste spam example
   → Show explanation & keywords

3. SMS Detection (1m)
   → Paste scam SMS
   → Highlight risk factors

4. URL Scanner (1m)
   → Scan suspicious URL
   → Explain risk score

5. Analytics (30s)
   → Show charts

6. Model Performance (1m)
   → Explain accuracy metrics
```

---

## 📊 Project Stats

- **Files:** 50+
- **Code:** 5,000+ lines
- **Tests:** 25 unit tests
- **Pages:** 9 interactive
- **Models:** 2 trained
- **Dataset:** 5,572 + 60
- **Accuracy:** 98% + 83%

---

## ✅ Pre-Demo Checklist

- [ ] Models trained (check models/ folder)
- [ ] App runs without errors
- [ ] Test all main features
- [ ] Prepare example messages
- [ ] Prepare example URLs
- [ ] Review viva questions
- [ ] Check terminal works
- [ ] Browser opens correctly

---

## 🔗 Important URLs

- **App:** http://localhost:8501
- **Alternate:** http://localhost:8502 (if 8501 busy)
- **Docs:** README.md
- **Setup:** INSTALLATION_GUIDE.md

---

## 🎯 Key Features Summary

✅ Email spam detection
✅ SMS scam detection
✅ URL security scanning
✅ Bulk CSV processing
✅ Detection history
✅ Interactive analytics
✅ Model evaluation
✅ Modern UI
✅ Local database
✅ Export capability

---

## 💾 Backup Important Files

Before presenting, backup:
- `models/*.pkl` (trained models)
- `detection_history.db` (if has data)
- `dataset/*.csv` (original datasets)

---

**Quick Reference v1.0**  
**SpamGuard AI - Intelligent Security Detection**

*Keep this card handy during your presentation! 🛡️*
