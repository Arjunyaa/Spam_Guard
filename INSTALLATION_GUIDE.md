# 🛡️ SpamGuard AI - Installation Guide

## Quick Start (Windows)

### Method 1: Automated Setup (Recommended)

1. **Double-click `SETUP.bat`**
   - This will automatically:
     - Create a virtual environment
     - Install all dependencies
     - Train the URL model
   - Wait for "Setup Complete!" message

2. **Double-click `START_APP.bat`**
   - The application will open in your browser
   - Visit http://localhost:8501

### Method 2: Manual Setup

If the automated scripts don't work, follow these steps:

---

## Detailed Installation Steps

### Prerequisites

- **Windows 10/11** (or macOS/Linux with minor command adjustments)
- **Python 3.8 or higher** installed
- **Internet connection** for downloading packages

### Step 1: Verify Python Installation

Open Command Prompt (CMD) and type:

```cmd
python --version
```

You should see something like `Python 3.x.x`. If not, download Python from [python.org](https://www.python.org/downloads/).

**Important:** During Python installation, check "Add Python to PATH"!

---

### Step 2: Navigate to Project Folder

```cmd
cd "C:\Users\aarju\Downloads\ML Project"
```

Replace with your actual project location.

---

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

This creates a folder called `venv` containing an isolated Python environment.

---

### Step 4: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

**Note:** You must activate the virtual environment every time you open a new terminal.

---

### Step 5: Install Dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- streamlit
- pandas
- numpy
- scikit-learn
- plotly
- joblib

Installation takes 2-5 minutes depending on your internet speed.

---

### Step 6: Verify Installation

```cmd
pip list
```

You should see all the required packages listed.

---

### Step 7: Train URL Model

```cmd
python training\train_url_model.py
```

This will:
- Load the URL dataset (60 samples)
- Train the LinearSVC classifier
- Save models to `models/` folder
- Display performance metrics

Expected output: ~83% accuracy, training takes ~5 seconds.

**Note:** The message model (`message_model.pkl`) is already trained and included in the `models/` folder.

---

### Step 8: Run Tests (Optional but Recommended)

```cmd
python tests\run_all_tests.py
```

All tests should pass (✅). If any fail, check error messages.

---

### Step 9: Start the Application

```cmd
streamlit run app.py
```

The application will automatically open in your default browser at:
**http://localhost:8501**

---

## First Time Usage

1. **Dashboard** - View overall statistics (will be empty initially)
2. **Email Detection** - Test with the example emails provided
3. **SMS Detection** - Try the sample spam messages
4. **URL Scanner** - Analyze suspicious URLs
5. **Bulk Detection** - Upload CSV files for batch processing

---

## Troubleshooting

### Issue: "Python is not recognized"

**Solution:** Python is not in your PATH.
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH in Environment Variables

---

### Issue: "No module named 'streamlit'"

**Solution:** Virtual environment not activated or packages not installed.

```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Issue: "Model file not found"

**Solution:** Train the URL model first.

```cmd
python training\train_url_model.py
```

---

### Issue: "Port 8501 is already in use"

**Solution:** Another Streamlit app is running.
1. Close other terminals running Streamlit
2. Or use a different port:

```cmd
streamlit run app.py --server.port 8502
```

---

### Issue: "Permission denied" on Windows

**Solution:** Run Command Prompt as Administrator.

---

### Issue: scikit-learn version warning

**Solution:** Update scikit-learn:

```cmd
pip install --upgrade scikit-learn
```

Then retrain models:

```cmd
python training\train_url_model.py
```

---

## Stopping the Application

Press `Ctrl + C` in the terminal where Streamlit is running.

---

## Running After First Installation

Every time you want to use the app:

**Option 1: Use the batch file**
```
Double-click START_APP.bat
```

**Option 2: Manual start**
```cmd
cd "C:\Users\aarju\Downloads\ML Project"
venv\Scripts\activate
streamlit run app.py
```

---

## File Structure After Installation

```
ML Project/
│
├── venv/                          ← Virtual environment (created)
│
├── models/
│   ├── message_model.pkl          ← Message spam classifier (existing)
│   ├── message_vectorizer.pkl     ← TF-IDF vectorizer (existing)
│   ├── url_model.pkl              ← URL classifier (created in Step 7)
│   └── url_vectorizer.pkl         ← URL vectorizer (created in Step 7)
│
├── detection_history.db           ← SQLite database (created on first use)
│
├── app.py                         ← Main application
├── requirements.txt               ← Dependencies list
├── SETUP.bat                      ← Automated setup script
├── START_APP.bat                  ← Quick start script
└── README.md                      ← Full documentation
```

---

## Updating the Application

If you make changes or pull updates:

1. Activate virtual environment
2. Install any new dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
3. Retrain models if datasets changed
4. Restart the application

---

## Uninstallation

To remove the application:

1. Delete the entire project folder
2. (Optional) Uninstall Python if not needed for other projects

---

## macOS/Linux Installation

For macOS/Linux users, replace commands as follows:

**Activate virtual environment:**
```bash
source venv/bin/activate
```

**Navigate:**
```bash
cd ~/Downloads/ML\ Project/
```

**Run Python:**
```bash
python3 instead of python
```

All other steps are the same.

---

## Additional Configuration

### Change Default Port

Edit the start command:
```cmd
streamlit run app.py --server.port 8080
```

### Enable Dark Theme

Streamlit uses system theme by default. To force dark mode:
```cmd
streamlit run app.py --theme.base dark
```

### Run in Browser Only

To prevent auto-opening browser:
```cmd
streamlit run app.py --server.headless true
```

---

## Performance Tips

1. **First load is slow:** Streamlit loads all components. Subsequent pages load faster.

2. **Large CSV files:** Process in smaller batches (<500 rows at a time).

3. **Memory usage:** Close unused browser tabs running the app.

4. **Database size:** Clear history periodically from the History page.

---

## Getting Help

1. **Check README.md** for comprehensive documentation
2. **Run tests** to verify installation: `python tests\run_all_tests.py`
3. **Check error messages** in the terminal
4. **Review Troubleshooting** section above

---

## System Requirements

- **OS:** Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python:** 3.8, 3.9, 3.10, 3.11, 3.12
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 500MB for project + dependencies
- **Browser:** Chrome, Firefox, Edge, Safari (latest versions)

---

## Important Notes

⚠️ **Security:**
- All processing is done locally
- No data is sent to external servers
- URLs are analyzed without visiting them
- Database stored locally (detection_history.db)

⚠️ **Accuracy:**
- Model accuracy: ~98% for message detection
- URL dataset is small (60 samples)
- Use heuristic analysis for better URL detection
- Cannot detect all sophisticated attacks

⚠️ **Educational Purpose:**
- This is a college project/portfolio demonstration
- Not suitable for production security systems without enhancements
- Always verify suspicious content through official channels

---

## Success Checklist

After installation, you should be able to:

- [ ] Run `python --version` and see Python 3.8+
- [ ] Activate virtual environment (see `(venv)` in prompt)
- [ ] See all packages with `pip list`
- [ ] Find 4 .pkl files in `models/` folder
- [ ] Run tests successfully
- [ ] Open app in browser at http://localhost:8501
- [ ] Analyze a test message and see results
- [ ] Scan a test URL and see risk score

---

## Next Steps After Installation

1. **Explore the Dashboard** - Familiarize yourself with the UI
2. **Try Examples** - Use provided example messages
3. **Test URL Scanner** - Analyze some real URLs (carefully!)
4. **Review Analytics** - Generate some data and view charts
5. **Read README.md** - Understand the technical details
6. **Prepare for Viva** - Review the Q&A section

---

## Contact & Support

For issues specific to this installation:
1. Check Python installation and PATH
2. Ensure virtual environment is activated
3. Verify all dependencies installed
4. Check error messages in terminal
5. Review Streamlit documentation

---

**Installation complete! Enjoy using SpamGuard AI! 🛡️**

**For detailed usage and technical information, see README.md**
