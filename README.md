# Voice Dictation Tool

A lightweight, floating voice-to-text dictation tool for Windows that seamlessly integrates with any application. Simply click to record, speak, and watch your words appear wherever your cursor is focused.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🎤 Floating Widget**: Always-on-top microphone button that can be dragged anywhere on screen
- **🎯 Universal Compatibility**: Works with any text field in any application
- **🚀 Multiple Versions**:
  - **Advanced**: Full-featured with system tray, settings dialog, and hotkey support
  - **Streaming**: Ultra-fast real-time transcription with word-by-word output
  - **Simple**: Lightweight basic version with core functionality
- **🌍 Multi-language Support**: Supports multiple languages including English, Spanish, French, German, and Italian
- **⚙️ Highly Configurable**: JSON-based configuration for customizing behavior and appearance
- **⌨️ Global Hotkey**: Toggle recording from anywhere with customizable keyboard shortcuts

## 🖼️ Screenshots

<details>
<summary>Click to view interface</summary>

The application features a minimal floating interface:
- Blue microphone icon when idle
- Red microphone icon when recording
- Draggable to any screen position
- Optional system tray integration (Advanced version)

</details>

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-dictation-tool.git
cd voice-dictation-tool

# Install dependencies
pip install -r requirements.txt

# Run the application
python voice_dictation_advanced.py  # Full-featured version
# OR
python voice_dictation_streaming.py  # Fastest version
# OR
python voice_dictation_simple.py     # Basic version
```

## 📋 Requirements

- Python 3.8 or higher
- Windows 10/11
- Working microphone
- Internet connection (for Google Speech Recognition)

## 🛠️ Installation

### Method 1: Using pip (Recommended)

```bash
pip install -r requirements.txt
```

### Method 2: Using the installer batch file

```batch
install.bat
```

### Method 3: Manual installation

```bash
pip install SpeechRecognition==3.10.4
pip install pyaudio==0.2.14
pip install pynput==1.7.7
pip install PyQt5==5.15.11
pip install pillow==10.4.0
pip install pystray==0.19.5
pip install keyboard==0.13.5
pip install pyperclip==1.9.0
```

## 📖 Usage

### Basic Operation

1. **Start the application** using one of the Python scripts or `run.bat`
2. **Click the microphone button** to start recording (icon turns red)
3. **Speak clearly** into your microphone
4. **Click again** to stop recording
5. **Watch your text appear** in the currently focused text field

### Version Comparison

| Feature | Advanced | Streaming | Simple |
|---------|----------|-----------|---------|
| System Tray | ✅ | ❌ | ❌ |
| Settings Dialog | ✅ | ❌ | ❌ |
| Global Hotkey | ✅ | ❌ | ❌ |
| Real-time Output | ❌ | ✅ | ❌ |
| Config File | ✅ | ❌ | ❌ |
| Resource Usage | Medium | Low | Lowest |
| Response Time | Normal | Fastest | Normal |

### Keyboard Shortcuts

- **Ctrl+Shift+D**: Toggle recording (Advanced version, customizable)
- **Right-click** on icon: Access context menu (Advanced version)

## ⚙️ Configuration

The Advanced version uses `config.json` for customization:

```json
{
    "language": "en-US",
    "auto_punctuation": true,
    "hotkey": "ctrl+shift+d",
    "theme": {
        "primary_color": "#2196F3",
        "recording_color": "#FF5252",
        "icon_size": 60
    },
    "recognition": {
        "timeout": 1,
        "phrase_time_limit": 10,
        "energy_threshold": 300
    }
}
```

### Available Languages

- `en-US` - English (United States)
- `en-GB` - English (United Kingdom)
- `es-ES` - Spanish (Spain)
- `fr-FR` - French (France)
- `de-DE` - German (Germany)
- `it-IT` - Italian (Italy)
- And many more...

## 🔧 Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   - Install Visual C++ Build Tools
   - Or use pre-built wheel: `pip install pipwin && pipwin install pyaudio`

2. **No audio detected**
   - Check Windows microphone permissions
   - Ensure default microphone is set correctly
   - Try adjusting `energy_threshold` in config

3. **Recognition errors**
   - Check internet connection
   - Speak more clearly and closer to microphone
   - Adjust `phrase_time_limit` for longer sentences

4. **Application won't start**
   - Ensure all dependencies are installed
   - Check for Python version compatibility (3.8+)
   - Run with `python -u` for debugging output

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SpeechRecognition](https://github.com/Uberi/speech_recognition) for the speech recognition functionality
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pystray](https://github.com/moses-palmer/pystray) for system tray integration
- Google Speech Recognition API for transcription services

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/voice-dictation-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/voice-dictation-tool/discussions)

---

Made with ❤️ for the community