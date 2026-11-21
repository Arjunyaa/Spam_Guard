@echo off
echo =========================================
echo   SpamGuard AI - Starting Application
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run SETUP.bat first.
    pause
    exit
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if models exist
if not exist "models\message_model.pkl" (
    echo Message model not found!
    echo Please run SETUP.bat first.
    pause
    exit
)

if not exist "models\url_model.pkl" (
    echo URL model not found!
    echo Please run training\train_url_model.py first.
    pause
    exit
)

echo Starting SpamGuard AI...
echo.
echo The application will open in your default browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
