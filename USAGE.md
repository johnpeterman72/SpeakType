# Usage Guide

This comprehensive guide covers all aspects of using the Voice Dictation Tool.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Version-Specific Features](#version-specific-features)
5. [Configuration](#configuration)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Use Cases](#use-cases)
8. [Keyboard Shortcuts](#keyboard-shortcuts)
9. [FAQ](#faq)

## Getting Started

### Launching the Application

#### Using run.bat (Recommended for beginners)
1. Double-click `run.bat`
2. Select your preferred version:
   - Press `1` for Advanced (full features)
   - Press `2` for Streaming (fastest)
   - Press `3` for Simple (lightweight)

#### Direct Python execution
```cmd
# Advanced version with all features
python voice_dictation_advanced.py

# Streaming version for real-time transcription
python voice_dictation_streaming.py

# Simple version for basic functionality
python voice_dictation_simple.py
```

#### Using batch shortcuts
- Double-click `start_streaming.bat` for quick streaming version launch

### First Run

1. A small floating microphone icon will appear on your screen
2. The icon can be dragged to any position
3. It will stay on top of all other windows
4. Blue icon = Ready to record
5. Red icon = Currently recording

## Basic Usage

### Recording Speech

1. **Position your cursor** where you want text to appear (any text field, document, etc.)
2. **Click the microphone icon** - it turns red to indicate recording
3. **Speak clearly** into your microphone
4. **Click again** to stop recording
5. **Wait briefly** - your speech will be transcribed and typed automatically

### Moving the Widget

- **Click and drag** the microphone icon to reposition it
- The position is remembered during the session
- Place it somewhere convenient but unobtrusive

### Stopping a Recording

- Click the red microphone icon
- Or wait for automatic timeout (configurable)
- The icon returns to blue when ready

## Advanced Features

### System Tray Integration (Advanced Version Only)

1. **Right-click** the microphone icon
2. Select **"Minimize to Tray"**
3. Access from the system tray (near the clock)
4. Double-click tray icon to restore

### Settings Dialog (Advanced Version Only)

1. **Right-click** the microphone icon
2. Select **"Settings"**
3. Configure:
   - **Language**: Choose recognition language
   - **Timeout**: How long to wait for speech
   - **Phrase Time Limit**: Maximum recording duration
   - **Auto-punctuation**: Automatic period/comma insertion
   - **Hotkey**: Global keyboard shortcut

### Global Hotkey (Advanced Version Only)

- Default: `Ctrl+Shift+D`
- Works from anywhere in Windows
- Toggle recording without clicking
- Customizable in settings

### Real-time Streaming (Streaming Version Only)

- Words appear as you speak
- No need to stop recording for transcription
- Lowest latency option
- Best for continuous dictation

## Version-Specific Features

### Advanced Version

**Best for**: Users who want full control and features

Features:
- ✅ System tray support
- ✅ Settings dialog
- ✅ Global hotkey
- ✅ Configuration file
- ✅ Multi-language support
- ✅ Auto-punctuation
- ✅ Customizable timeouts

### Streaming Version

**Best for**: Fast, real-time transcription

Features:
- ✅ Word-by-word output
- ✅ Minimal latency
- ✅ Background listening
- ✅ Clipboard-based insertion
- ❌ No system tray
- ❌ No settings dialog

### Simple Version

**Best for**: Minimal resource usage

Features:
- ✅ Basic recording
- ✅ Lightweight
- ✅ Stable operation
- ❌ No extra features
- ❌ No configuration

## Configuration

### config.json Structure (Advanced Version)

```json
{
    "language": "en-US",              // Recognition language
    "auto_punctuation": true,         // Add periods automatically
    "hotkey": "ctrl+shift+d",         // Global hotkey combination
    "theme": {
        "primary_color": "#2196F3",   // Blue icon color
        "recording_color": "#FF5252", // Red recording color
        "icon_size": 60               // Widget size in pixels
    },
    "recognition": {
        "timeout": 1,                 // Seconds to wait for speech
        "phrase_time_limit": 10,      // Max recording seconds
        "energy_threshold": 300       // Microphone sensitivity
    }
}
```

### Language Codes

Common language codes for the `language` setting:

- `en-US` - English (United States)
- `en-GB` - English (United Kingdom)
- `en-AU` - English (Australia)
- `es-ES` - Spanish (Spain)
- `es-MX` - Spanish (Mexico)
- `fr-FR` - French (France)
- `de-DE` - German (Germany)
- `it-IT` - Italian (Italy)
- `pt-BR` - Portuguese (Brazil)
- `zh-CN` - Chinese (Simplified)
- `ja-JP` - Japanese
- `ko-KR` - Korean

### Adjusting Microphone Sensitivity

If the tool isn't detecting your voice:

1. Lower `energy_threshold` (e.g., 100-200) for quiet environments
2. Raise `energy_threshold` (e.g., 500-1000) for noisy environments
3. Restart the application after changes

## Tips and Best Practices

### For Best Recognition

1. **Speak clearly and naturally**
   - Don't speak too fast or too slow
   - Maintain consistent volume
   - Minimize background noise

2. **Use a quality microphone**
   - Headset microphones work best
   - Position mic 1-2 inches from mouth
   - Avoid laptop built-in mics if possible

3. **Optimize your environment**
   - Close windows to reduce outside noise
   - Turn off fans or AC if possible
   - Use in a quiet room

### For Efficient Use

1. **Learn the hotkey** (Advanced version)
   - Much faster than clicking
   - Works from any application
   - Customize to your preference

2. **Position the widget strategically**
   - Near where you usually type
   - But not blocking important content
   - Consider screen edges

3. **Use appropriate version**
   - Streaming for long dictation sessions
   - Advanced for feature-rich experience
   - Simple for resource-constrained systems

### Common Commands

The tool recognizes common punctuation commands:

- Say "period" → .
- Say "comma" → ,
- Say "question mark" → ?
- Say "exclamation mark" → !
- Say "new line" → ↵
- Say "new paragraph" → ↵↵

## Use Cases

### Document Writing
- Draft emails quickly
- Write reports hands-free
- Take notes during calls

### Coding
- Add comments to code
- Write documentation
- Quick variable naming

### Accessibility
- Reduce typing strain
- Alternative input method
- Hands-free computer use

### Creative Writing
- Capture ideas quickly
- Stream-of-consciousness writing
- Dialogue transcription

### Data Entry
- Form filling
- Spreadsheet input
- Database entry

## Keyboard Shortcuts

### Global Shortcuts (System-wide)

| Shortcut | Action | Version |
|----------|--------|---------|
| Ctrl+Shift+D | Toggle recording | Advanced |

### Application Shortcuts

| Action | Method | Version |
|--------|--------|---------|
| Start/Stop Recording | Click microphone | All |
| Move widget | Drag microphone | All |
| Open menu | Right-click | Advanced |
| Exit | Right-click → Exit | All |

## FAQ

### Q: Why isn't my speech being recognized?

**A:** Check these common issues:
1. Internet connection (required for Google Speech Recognition)
2. Microphone permissions in Windows
3. Microphone is default recording device
4. Speak louder or adjust `energy_threshold`

### Q: Can I use this offline?

**A:** No, the tool requires internet for Google's speech recognition service.

### Q: Why is there a delay before text appears?

**A:** The tool waits briefly to ensure you've finished speaking. Use the Streaming version for real-time output.

### Q: Can I dictate in multiple languages?

**A:** Yes, change the language in settings (Advanced version) or config.json.

### Q: How do I add punctuation?

**A:** Either:
- Enable auto-punctuation in settings
- Say punctuation marks explicitly
- Add manually after dictation

### Q: Can I use this with multiple monitors?

**A:** Yes, drag the widget to any monitor. It remembers position during the session.

### Q: Is my audio data private?

**A:** Audio is sent to Google for processing. No local storage occurs.

### Q: Can I customize the appearance?

**A:** Yes, edit theme colors in config.json (Advanced version).

### Q: Why does antivirus flag the app?

**A:** The keyboard module may trigger false positives. Add an exception for the app folder.

### Q: How do I update the application?

**A:** Download the latest version and replace the Python files. Keep your config.json.

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| No microphone detected | Check Windows sound settings |
| Text appears in wrong place | Click destination field first |
| Recording stops too quickly | Increase `phrase_time_limit` |
| Too sensitive to noise | Increase `energy_threshold` |
| Hotkey not working | Run as administrator |
| Widget disappeared | Check system tray (Advanced) |

## Advanced Configuration

### Creating Custom Themes

Edit config.json:
```json
"theme": {
    "primary_color": "#4CAF50",    // Green theme
    "recording_color": "#FFC107",  // Amber recording
    "icon_size": 80                // Larger icon
}
```

### Performance Tuning

For faster response:
```json
"recognition": {
    "timeout": 0.5,           // Shorter timeout
    "phrase_time_limit": 5,   // Shorter phrases
    "energy_threshold": 100   // More sensitive
}
```

### Multi-user Setup

1. Copy the folder for each user
2. Customize config.json per user
3. Use different hotkeys to avoid conflicts

## Getting Help

- Check the [Installation Guide](INSTALLATION.md) for setup issues
- See the [README](README.md) for overview
- Report bugs on [GitHub Issues](https://github.com/yourusername/voice-dictation-tool/issues)