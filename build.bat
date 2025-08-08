@echo off
echo.
echo ========================================
echo   Macro Recorder - .exe Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo 🔨 Building .exe file...
python build_exe.py

echo.
echo ✅ Build process completed!
echo Check the output above for results.
echo.
pause
