import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QColor
import speech_recognition as sr
import pynput.keyboard

class SignalEmitter(QObject):
    text_ready = pyqtSignal(str)
    status_update = pyqtSignal(str)

class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.keyboard_controller = pynput.keyboard.Controller()
        self.signals = SignalEmitter()
        self.signals.text_ready.connect(self.type_text)
        self.signals.status_update.connect(self.update_status)
        
        self.init_ui()
        self.init_microphone()
        
    def init_ui(self):
        self.setWindowTitle('Voice Dictation')
        self.setFixedSize(80, 80)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        self.mic_button = QPushButton()
        self.mic_button.setFixedSize(60, 60)
        self.mic_button.clicked.connect(self.toggle_recording)
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
        
        layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        
        self.create_mic_icon()
        self.show()
        
        desktop_geometry = QApplication.desktop().availableGeometry()
        self.move(desktop_geometry.width() - 100, desktop_geometry.height() // 2)
        
        self.oldPos = QPoint()
        
    def init_microphone(self):
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Microphone initialization error: {e}")
            self.signals.status_update.emit("Microphone error")
            
    def create_mic_icon(self):
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.is_recording:
            painter.setBrush(QBrush(QColor('#FF5252')))
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
            
    def toggle_recording(self):
        if not self.microphone:
            self.init_microphone()
            if not self.microphone:
                return
                
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        self.is_recording = True
        self.create_mic_icon()
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
        
        self.recognition_thread = threading.Thread(target=self.record_audio)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        self.signals.status_update.emit("Listening...")
        
    def stop_recording(self):
        self.is_recording = False
        self.create_mic_icon()
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
        
        self.signals.status_update.emit("Stopped")
        
    def record_audio(self):
        if not self.microphone:
            return
            
        with self.microphone as source:
            while self.is_recording:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    threading.Thread(target=self.recognize_speech, args=(audio,)).start()
                except sr.WaitTimeoutError:
                    pass
                except Exception as e:
                    print(f"Error recording: {e}")
                    
    def recognize_speech(self, audio):
        try:
            self.signals.status_update.emit("Processing...")
            text = self.recognizer.recognize_google(audio)
            
            if text:
                self.signals.text_ready.emit(text)
                self.signals.status_update.emit(f"Typed: {text[:20]}...")
                
        except sr.UnknownValueError:
            self.signals.status_update.emit("Could not understand")
        except sr.RequestError as e:
            self.signals.status_update.emit(f"Error: {e}")
        except Exception as e:
            print(f"Recognition error: {e}")
            
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

def main():
    app = QApplication(sys.argv)
    widget = FloatingWidget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()