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

REM Launch menu
echo ==========================================
echo Choose launch option:
echo ==========================================
echo 1. Launch Web Application (HTML/Flask)
echo 2. Run Terminal Test
echo 3. Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Launching Flask application...
    echo The app will open in your browser at http://localhost:5000
    echo.
    python server.py
) else if "%choice%"=="2" (
    echo.
    set /p img_path="Enter path to test image: "
    python test\test_pipeline.py "%img_path%"
) else if "%choice%"=="3" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Exiting...
    exit /b 1
)