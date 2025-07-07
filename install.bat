@echo off
echo Installing Voice Dictation Software...
echo.

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies. Please ensure Python and pip are installed.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing additional build tools...
pip install cx_Freeze
if %errorlevel% neq 0 (
    echo Error installing cx_Freeze.
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo To run the application:
echo   - Basic version: python voice_dictation.py
echo   - Advanced version: python voice_dictation_advanced.py
echo.
echo To build executable: python setup.py build
echo.
pause