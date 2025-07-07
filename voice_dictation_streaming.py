import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor, QPen
import speech_recognition as sr
import pynput.keyboard
import pyperclip

class SignalEmitter(QObject):
    text_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)

class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.recognizer = sr.Recognizer()
        # Ultra-fast settings
        self.recognizer.pause_threshold = 0.2
        self.recognizer.phrase_threshold = 0.05
        self.recognizer.non_speaking_duration = 0.1
        self.recognizer.energy_threshold = 50
        self.recognizer.dynamic_energy_threshold = False
        
        self.microphone = None
        self.keyboard_controller = pynput.keyboard.Controller()
        self.signals = SignalEmitter()
        self.signals.text_ready.connect(self.type_text)
        self.signals.status_update.connect(self.update_status)
        
        self.stop_listening = None
        self.mic_stream = None
        
        self.init_ui()
        self.init_microphone()
        
    def init_ui(self):
        self.setWindowTitle('Voice Dictation')
        self.setFixedSize(120, 80)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(5)
        
        # Microphone button
        self.mic_button = QPushButton()
        self.mic_button.setFixedSize(60, 60)
        self.mic_button.clicked.connect(self.toggle_recording)
        self.mic_button.setCursor(Qt.PointingHandCursor)
        self.update_button_style()
        
        # Close button
        self.close_button = QPushButton()
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                border-radius: 15px;
                border: 2px solid #D32F2F;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
            QPushButton:pressed {
                background-color: #B71C1C;
            }
        """)
        
        main_layout.addWidget(self.mic_button)
        main_layout.addWidget(self.close_button)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)
        
        self.create_mic_icon()
        self.create_close_icon()
        self.show()
        
        desktop_geometry = QApplication.desktop().availableGeometry()
        self.move(desktop_geometry.width() - 140, desktop_geometry.height() // 2)
        
        self.oldPos = QPoint()
        
    def init_microphone(self):
        try:
            self.microphone = sr.Microphone()
            # No calibration for fastest startup
            self.signals.status_update.emit("Ready")
        except Exception as e:
            print(f"Microphone initialization error: {e}")
            self.signals.status_update.emit("Microphone error")
            
    def update_button_style(self):
        if self.is_recording:
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF5252;
                    border-radius: 30px;
                    border: 3px solid #D32F2F;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                }
            """)
        else:
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    border-radius: 30px;
                    border: 3px solid #1976D2;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
        
    def create_mic_icon(self):
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor('#FFFFFF')))
        painter.setPen(Qt.NoPen)
        
        painter.drawEllipse(15, 5, 10, 15)
        painter.drawRect(18, 20, 4, 8)
        painter.drawRect(10, 25, 20, 2)
        painter.drawRect(19, 28, 2, 5)
        
        painter.end()
        
        self.mic_button.setIcon(QIcon(pixmap))
        self.mic_button.setIconSize(pixmap.size())
        
    def create_close_icon(self):
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor('#FFFFFF'), 2))
        
        painter.drawLine(5, 5, 15, 15)
        painter.drawLine(15, 5, 5, 15)
        
        painter.end()
        
        self.close_button.setIcon(QIcon(pixmap))
        self.close_button.setIconSize(pixmap.size())
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos() - self.pos()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.oldPos:
            self.move(event.globalPos() - self.oldPos)
            
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        if not self.microphone:
            return
            
        self.is_recording = True
        self.update_button_style()
        self.signals.status_update.emit("Listening...")
        
        # Start listening in background
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self.callback,
            phrase_time_limit=2  # Short phrases for quick response
        )
        
    def stop_recording(self):
        self.is_recording = False
        self.update_button_style()
        self.signals.status_update.emit("Stopped")
        
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)
            self.stop_listening = None
            
    def callback(self, recognizer, audio):
        if not self.is_recording:
            return
            
        try:
            # Process in separate thread to not block
            threading.Thread(target=self.process_audio, args=(audio,), daemon=True).start()
        except Exception as e:
            print(f"Callback error: {e}")
            
    def process_audio(self, audio):
        try:
            # Fast recognition
            text = self.recognizer.recognize_google(audio, language='en-US')
            
            if text and self.is_recording:
                self.signals.text_ready.emit(text)
                
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            self.signals.status_update.emit("API Error")
        except Exception as e:
            print(f"Recognition error: {e}")
            
    def type_text(self, text):
        # Direct typing for even faster response
        for word in text.split():
            pyperclip.copy(word + ' ')
            
            self.keyboard_controller.press(pynput.keyboard.Key.ctrl)
            self.keyboard_controller.press('v')
            self.keyboard_controller.release('v')
            self.keyboard_controller.release(pynput.keyboard.Key.ctrl)
            
            time.sleep(0.01)  # Minimal delay between words
            
        self.signals.status_update.emit("Ready")
        
    def update_status(self, status):
        self.setToolTip(status)
        
    def closeEvent(self, event):
        self.stop_recording()
        event.accept()

def main():
    app = QApplication(sys.argv)
    widget = FloatingWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()