# Installation Guide

This guide will walk you through the process of installing the Voice Dictation Tool on your Windows system.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Python Installation](#python-installation)
3. [Dependency Installation](#dependency-installation)
4. [Troubleshooting](#troubleshooting)
5. [Verification](#verification)

## System Requirements

Before installing, ensure your system meets these requirements:

- **Operating System**: Windows 10 or Windows 11
- **Python Version**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: ~500MB free space
- **Hardware**: Working microphone
- **Network**: Active internet connection (for speech recognition)

## Python Installation

### Step 1: Check if Python is installed

Open Command Prompt and run:
```cmd
python --version
```

If Python 3.8+ is installed, skip to [Dependency Installation](#dependency-installation).

### Step 2: Download Python

1. Visit [python.org](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer for Windows
3. **Important**: Choose the 64-bit installer

### Step 3: Install Python

1. Run the downloaded installer
2. ✅ **Check "Add Python to PATH"** at the bottom of the installer
3. Click "Install Now"
4. Wait for installation to complete

## Dependency Installation

### Method 1: Automated Installation (Recommended)

1. Open Command Prompt in the project directory
2. Run the installation script:
   ```cmd
   install.bat
   ```

This will automatically install all required dependencies.

### Method 2: Using pip

1. Open Command Prompt in the project directory
2. Run:
   ```cmd
   pip install -r requirements.txt
   ```

### Method 3: Manual Installation

Install each dependency individually:

```cmd
pip install SpeechRecognition==3.10.4
pip install pyaudio==0.2.14
pip install pynput==1.7.7
pip install PyQt5==5.15.11
pip install pillow==10.4.0
pip install pystray==0.19.5
pip install keyboard==0.13.5
pip install pyperclip==1.9.0
pip install setuptools==75.1.0
```

## Troubleshooting

### PyAudio Installation Issues

PyAudio often requires additional steps on Windows:

#### Option 1: Using pipwin (Easiest)
```cmd
pip install pipwin
pipwin install pyaudio
```

#### Option 2: Using pre-built wheel
1. Visit [PyAudio Wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Download the appropriate wheel file:
   - For Python 3.8: `PyAudio‑0.2.11‑cp38‑cp38‑win_amd64.whl`
   - For Python 3.9: `PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`
   - For Python 3.10: `PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl`
3. Install using:
   ```cmd
   pip install path\to\downloaded\wheel\file.whl
   ```

#### Option 3: Install Visual C++ Build Tools
1. Download [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Install with "Desktop development with C++" workload
3. Retry `pip install pyaudio`

### PyQt5 Installation Issues

If PyQt5 fails to install:

```cmd
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install PyQt5
pip install PyQt5==5.15.11

# If still failing, try without version constraint
pip install PyQt5
```

### Permission Errors

If you encounter permission errors:

1. Run Command Prompt as Administrator
2. Or use the `--user` flag:
   ```cmd
   pip install --user -r requirements.txt
   ```

### SSL Certificate Errors

If you see SSL errors:

```cmd
# Upgrade certificates
pip install --upgrade certifi

# Or use trusted host
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

## Verification

After installation, verify everything is working:

### 1. Test Python Installation
```cmd
python --version
```
Should show Python 3.8 or higher.

### 2. Test Dependencies
Create a test file `test_install.py`:

```python
try:
    import speech_recognition as sr
    print("✓ SpeechRecognition installed")
except ImportError:
    print("✗ SpeechRecognition not installed")

try:
    import pyaudio
    print("✓ PyAudio installed")
except ImportError:
    print("✗ PyAudio not installed")

try:
    import PyQt5
    print("✓ PyQt5 installed")
except ImportError:
    print("✗ PyQt5 not installed")

try:
    import pynput
    print("✓ pynput installed")
except ImportError:
    print("✗ pynput not installed")

try:
    import PIL
    print("✓ Pillow installed")
except ImportError:
    print("✗ Pillow not installed")

try:
    import pystray
    print("✓ pystray installed")
except ImportError:
    print("✗ pystray not installed")

try:
    import keyboard
    print("✓ keyboard installed")
except ImportError:
    print("✗ keyboard not installed")

try:
    import pyperclip
    print("✓ pyperclip installed")
except ImportError:
    print("✗ pyperclip not installed")

print("\nAll dependencies checked!")
```

Run it:
```cmd
python test_install.py
```

All items should show ✓ checkmarks.

### 3. Test Microphone Access
```python
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Microphone is working!")
```

### 4. Run the Application
```cmd
python voice_dictation_simple.py
```

The floating microphone widget should appear on your screen.

## Post-Installation

### Windows Defender / Antivirus

Some antivirus software may flag the keyboard module. To resolve:

1. Add an exception for the project folder
2. Or temporarily disable real-time protection during installation

### Microphone Permissions

Ensure Python has microphone access:

1. Go to Windows Settings → Privacy → Microphone
2. Enable "Allow apps to access your microphone"
3. Enable "Allow desktop apps to access your microphone"

### Performance Optimization

For best performance:

1. Close unnecessary applications
2. Use a good quality microphone
3. Ensure stable internet connection
4. Consider using the Streaming version for fastest response

## Next Steps

Once installation is complete:

1. Read the [Usage Guide](USAGE.md) for detailed instructions
2. Check the main [README](README.md) for configuration options
3. Run `python voice_dictation_advanced.py` for the full-featured version

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Search [existing issues](https://github.com/yourusername/voice-dictation-tool/issues)
3. Create a new issue with:
   - Your Python version (`python --version`)
   - Error messages (full traceback)
   - Steps to reproduce the problem