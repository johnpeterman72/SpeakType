@echo off
title Voice Dictation Software
cls

echo ========================================
echo    Voice Dictation Software Launcher
echo ========================================
echo.
echo Select a version to run:
echo.
echo 1. Advanced Version (Full Features)
echo 2. Streaming Version (Fastest)
echo 3. Simple Version (Basic)
echo 4. Install Dependencies
echo 5. Exit
echo.
echo ========================================
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto optimized
if "%choice%"=="2" goto streaming
if "%choice%"=="3" goto simple
if "%choice%"=="4" goto install
if "%choice%"=="5" goto end

echo Invalid choice. Please try again.
pause
goto :eof

:optimized
echo.
echo Starting Advanced Version...
python voice_dictation_advanced.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start. Make sure Python is installed and dependencies are met.
    echo Run option 4 to install dependencies.
    pause
)
goto end

:streaming
echo.
echo Starting Streaming Version...
python voice_dictation_streaming.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start. Make sure Python is installed and dependencies are met.
    echo Run option 4 to install dependencies.
    pause
)
goto end

:simple
echo.
echo Starting Simple Version...
python voice_dictation_simple.py
if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start. Make sure Python is installed and dependencies are met.
    echo Run option 4 to install dependencies.
    pause
)
goto end

:install
echo.
echo Installing dependencies...
call install_fix.bat
echo.
echo Installation complete. You can now run the voice dictation software.
pause
goto :eof

:end
exit