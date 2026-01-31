@echo off
REM Quick Start Script for AI Waste Reuse Intelligence System (Windows)

echo ==========================================
echo AI Waste Reuse Intelligence System
echo Quick Start Setup
echo ==========================================
echo.

REM Check Python
echo Checking Python version...
python --version
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check API key
if "%GEMINI_API_KEY%"=="" (
    echo WARNING: GEMINI_API_KEY not set!
    echo.
    echo To set your API key in PowerShell:
    echo   $env:GEMINI_API_KEY="your-key-here"
    echo.
    echo Get a free key at: https://makersuite.google.com/app/apikey
    echo.
    pause
) else (
    echo API key detected
    echo.
)

REM Check environment
echo Running environment check...
python test\test_pipeline.py --check-env
echo.

REM Launch the application
echo ==========================================
echo Launching Web Application
echo ==========================================
echo.
echo Starting Flask server...
echo The app will open in your browser at http://localhost:5000
echo.
python server.py