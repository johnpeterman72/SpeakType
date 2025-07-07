import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "sys", "PyQt5", "speech_recognition", "pynput", "pystray", "PIL", "keyboard"],
    "include_files": ["config.json"],
    "excludes": ["tkinter"]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Voice Dictation",
    version="1.0",
    description="Voice to text dictation software for Windows",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("voice_dictation_advanced.py", base=base, shortcut_name="Voice Dictation",
                   shortcut_dir="DesktopFolder")
    ]
)