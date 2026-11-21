@echo off
echo =========================================
echo   SpamGuard AI - Initial Setup
echo =========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit
)

echo Python found!
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment!
    pause
    exit
)
echo Virtual environment created!
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing required packages...
echo This may take a few minutes...
echo.
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit
)
echo.
echo All packages installed successfully!
echo.

REM Train URL model
echo Training URL classification model...
echo.
python training\train_url_model.py
if errorlevel 1 (
    echo URL model training failed!
    pause
    exit
)
echo.

echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo You can now run the application using START_APP.bat
echo or manually with: streamlit run app.py
echo.
pause
