import sys
import json
import threading
import queue
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QMenu, 
                             QDialog, QLabel, QComboBox, 
                             QSpinBox, QHBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor
import speech_recognition as sr
import pynput.keyboard
import keyboard
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageDraw

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.config = self.load_config()
        
    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return self.get_default_config()
            
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def get_default_config(self):
        return {
            "language": "en-US",
            "auto_punctuation": True,
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

class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Settings')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel('Language:'))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE', 'it-IT'])
        self.lang_combo.setCurrentText(self.config_manager.config['language'])
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)
        
        self.auto_punct_check = QCheckBox('Auto Punctuation')
        self.auto_punct_check.setChecked(self.config_manager.config['auto_punctuation'])
        layout.addWidget(self.auto_punct_check)
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel('Timeout (seconds):'))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(self.config_manager.config['recognition']['timeout'])
        timeout_layout.addWidget(self.timeout_spin)
        layout.addLayout(timeout_layout)
        
        phrase_layout = QHBoxLayout()
        phrase_layout.addWidget(QLabel('Max phrase length (seconds):'))
        self.phrase_spin = QSpinBox()
        self.phrase_spin.setRange(5, 30)
        self.phrase_spin.setValue(self.config_manager.config['recognition']['phrase_time_limit'])
        phrase_layout.addWidget(self.phrase_spin)
        layout.addLayout(phrase_layout)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(self.save_settings)
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def save_settings(self):
        self.config_manager.config['language'] = self.lang_combo.currentText()
        self.config_manager.config['auto_punctuation'] = self.auto_punct_check.isChecked()
        self.config_manager.config['recognition']['timeout'] = self.timeout_spin.value()
        self.config_manager.config['recognition']['phrase_time_limit'] = self.phrase_spin.value()
        self.config_manager.save_config()
        self.accept()

class SignalEmitter(QObject):
    text_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)

class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.is_recording = False
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio_queue = queue.Queue()
        self.keyboard_controller = pynput.keyboard.Controller()
        self.signals = SignalEmitter()
        self.signals.text_ready.connect(self.type_text)
        self.signals.status_update.connect(self.update_status)
        
        self.init_ui()
        self.init_speech_recognition()
        self.setup_hotkey()
        
    def init_ui(self):
        self.setWindowTitle('Voice Dictation')
        size = self.config_manager.config['theme']['icon_size'] + 20
        self.setFixedSize(size, size)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        self.mic_button = QPushButton()
        btn_size = self.config_manager.config['theme']['icon_size']
        self.mic_button.setFixedSize(btn_size, btn_size)
        self.mic_button.clicked.connect(self.toggle_recording)
        self.update_button_style()
        
        layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        
        self.create_mic_icon()
        self.show()
        
        desktop_geometry = QApplication.desktop().availableGeometry()
        self.move(desktop_geometry.width() - 100, desktop_geometry.height() // 2)
        
        self.oldPos = QPoint()
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
    def show_context_menu(self, position):
        menu = QMenu()
        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self.show_settings)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)
        menu.exec_(self.mapToGlobal(position))
        
    def show_settings(self):
        dialog = SettingsDialog(self.config_manager, self)
        if dialog.exec_():
            self.init_speech_recognition()
            self.setup_hotkey()
            
    def update_button_style(self):
        primary = self.config_manager.config['theme']['primary_color']
        recording = self.config_manager.config['theme']['recording_color']
        
        if self.is_recording:
            self.mic_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {recording};
                    border-radius: {self.mic_button.width()//2}px;
                    border: 3px solid #D32F2F;
                }}
                QPushButton:hover {{
                    background-color: #D32F2F;
                }}
            """)
        else:
            self.mic_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {primary};
                    border-radius: {self.mic_button.width()//2}px;
                    border: 3px solid #1976D2;
                }}
                QPushButton:hover {{
                    background-color: #1976D2;
                }}
                QPushButton:pressed {{
                    background-color: #0D47A1;
                }}
            """)
        
    def create_mic_icon(self):
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.is_recording:
            painter.setBrush(QBrush(QColor('#FFFFFF')))
        else:
            painter.setBrush(QBrush(QColor('#FFFFFF')))
            
        painter.setPen(Qt.NoPen)
        
        painter.drawEllipse(15, 5, 10, 15)
        painter.drawRect(18, 20, 4, 8)
        
        painter.drawRect(10, 25, 20, 2)
        
        painter.drawRect(19, 28, 2, 5)
        
        painter.end()
        
        self.mic_button.setIcon(QIcon(pixmap))
        self.mic_button.setIconSize(pixmap.size())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos() - self.pos()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos:
            self.move(event.globalPos() - self.oldPos)
            
    def init_speech_recognition(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.recognizer.energy_threshold = self.config_manager.config['recognition']['energy_threshold']
            
        self.recognition_thread = None
        
    def setup_hotkey(self):
        try:
            keyboard.add_hotkey(self.config_manager.config['hotkey'], self.toggle_recording)
        except:
            pass
            
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        self.is_recording = True
        self.create_mic_icon()
        self.update_button_style()
        
        self.recognition_thread = threading.Thread(target=self.record_audio)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        self.signals.status_update.emit("Listening...")
        
    def stop_recording(self):
        self.is_recording = False
        self.create_mic_icon()
        self.update_button_style()
        
        self.signals.status_update.emit("Stopped")
        
    def record_audio(self):
        with self.microphone as source:
            while self.is_recording:
                try:
                    timeout = self.config_manager.config['recognition']['timeout']
                    phrase_limit = self.config_manager.config['recognition']['phrase_time_limit']
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                    
                    threading.Thread(target=self.recognize_speech, args=(audio,)).start()
                    
                except sr.WaitTimeoutError:
                    pass
                except Exception as e:
                    print(f"Error recording: {e}")
                    
    def recognize_speech(self, audio):
        try:
            self.signals.status_update.emit("Processing...")
            
            language = self.config_manager.config['language']
            text = self.recognizer.recognize_google(audio, language=language)
            
            if text:
                if self.config_manager.config['auto_punctuation']:
                    text = self.add_punctuation(text)
                    
                self.signals.text_ready.emit(text)
                self.signals.status_update.emit(f"Typed: {text[:20]}...")
                
        except sr.UnknownValueError:
            self.signals.status_update.emit("Could not understand")
        except sr.RequestError as e:
            self.signals.status_update.emit(f"Error: {e}")
        except Exception as e:
            print(f"Recognition error: {e}")
            
    def add_punctuation(self, text):
        if text and text[-1] not in '.!?':
            text += '.'
        return text.capitalize()
        
    def type_text(self, text):
        time.sleep(0.1)
        
        for char in text:
            self.keyboard_controller.type(char)
            time.sleep(0.01)
            
        self.keyboard_controller.type(' ')
        
    def update_status(self, status):
        self.setToolTip(status)
        
    def closeEvent(self, event):
        self.is_recording = False
        event.accept()

class SystemTrayApp:
    def __init__(self, widget):
        self.widget = widget
        self.create_tray_icon()
        
    def create_tray_icon(self):
        image = Image.new('RGB', (64, 64), color='blue')
        draw = ImageDraw.Draw(image)
        draw.ellipse([16, 8, 48, 40], fill='white')
        draw.rectangle([28, 40, 36, 50], fill='white')
        draw.rectangle([20, 48, 44, 52], fill='white')
        
        menu = pystray.Menu(
            item('Show/Hide', self.toggle_window),
            item('Settings', self.show_settings),
            item('Exit', self.quit_app)
        )
        
        self.icon = pystray.Icon("voice_dictation", image, "Voice Dictation", menu)
        
        icon_thread = threading.Thread(target=self.icon.run)
        icon_thread.daemon = True
        icon_thread.start()
        
    def toggle_window(self, icon, item):
        if self.widget.isVisible():
            self.widget.hide()
        else:
            self.widget.show()
            
    def show_settings(self, icon, item):
        self.widget.show_settings()
            
    def quit_app(self, icon, item):
        self.icon.stop()
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    widget = FloatingWidget()
    tray_app = SystemTrayApp(widget)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()