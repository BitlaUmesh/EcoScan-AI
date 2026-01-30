@echo off
echo ==========================================
echo Fixing Ollama CUDA Error
echo ==========================================
echo.

echo Step 1: Stopping Ollama service...
taskkill /F /IM ollama.exe 2>nul
timeout /t 2 >nul

echo Step 2: Starting Ollama in CPU-only mode...
echo.
echo Setting environment variable to disable GPU...
set OLLAMA_NUM_GPU=0

echo.
echo Starting Ollama service (CPU mode)...
echo This will run Ollama without GPU acceleration.
echo.
start "Ollama CPU Mode" cmd /k "set OLLAMA_NUM_GPU=0 && ollama serve"

echo.
echo ==========================================
echo Ollama is now running in CPU mode
echo ==========================================
echo.
echo The CUDA error should be resolved.
echo You can now run the application with:
echo   streamlit run frontend\app.py
echo.
pause