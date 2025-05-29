from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
import cv2
import numpy as np
from game import ExpressionGame

class GameWindow(QMainWindow):
    def __init__(self, cam_index):
        super().__init__()
        self.game = ExpressionGame(cam_index)
        self.is_closing = False  # Add flag to track window state
        self.initUI()
        
    def initUI(self):
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)  # Add space between containers
        
        # Video container
        video_container = QFrame()
        video_container.setFrameStyle(QFrame.Shape.Box)
        video_container.setStyleSheet("QFrame { background-color: black; }")
        video_layout = QVBoxLayout(video_container)
        
        # Video feed label
        self.video_label = QLabel()
        self.video_label.setMinimumSize(1280, 720)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_layout.addWidget(self.video_label)
        
        # Add video container to main layout
        main_layout.addWidget(video_container)
        
        # Button container
        button_container = QFrame()
        button_container.setFixedHeight(80)  # Set fixed height for button area
        button_container.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        # Button layout
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)  # Space between buttons
        button_layout.setContentsMargins(20, 0, 20, 0)
        
        # Create and store buttons as instance variables
        self.start_btn = QPushButton("Start Game")
        self.landmark_btn = QPushButton("Toggle Landmarks")
        self.reset_btn = QPushButton("Reset Game")
        self.quit_btn = QPushButton("Quit")
        
        # Store buttons in a list for easy access
        self.buttons = [self.start_btn, self.landmark_btn, self.reset_btn, self.quit_btn]
        
        button_style = """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """
        
        # Add all buttons to layout
        for btn in self.buttons:
            btn.setStyleSheet(button_style)
            button_layout.addWidget(btn)
        
        # Add button container to main layout
        main_layout.addWidget(button_container)
        
        # Connect buttons
        self.start_btn.clicked.connect(self.start_game)
        self.landmark_btn.clicked.connect(self.toggle_landmarks)
        self.reset_btn.clicked.connect(self.reset_game)
        self.quit_btn.clicked.connect(self.close)

        # Initial button states
        self.reset_btn.setEnabled(False)
        
        # Window setup
        self.setWindowTitle('Swipe That Face!')
        self.setMinimumSize(1280, 820)  # 720 + button area + margins
        self.setStyleSheet("background-color: #2c3e50;")  # Dark background
        
        # Setup timer for video update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms = ~33fps
        
    def start_game(self):
        """Handle start button click"""
        self.game.start_game()
        self.start_btn.setEnabled(False)
        self.reset_btn.setEnabled(False)

    def update_frame(self):
        if self.is_closing:
            return
            
        frame = self.game.get_current_frame()
        if frame is not None:
            h, w = frame.shape[:2]
            q_img = QImage(frame.data, w, h, frame.strides[0], QImage.Format.Format_BGR888)
            self.video_label.setPixmap(QPixmap.fromImage(q_img))
            
            # Update button states only if window is still active
            try:
                if self.game.game_completed:
                    self.reset_btn.setEnabled(True)
                    self.start_btn.setEnabled(False)
                elif self.game.game_state == self.game.MENU:
                    self.start_btn.setEnabled(True)
                    self.reset_btn.setEnabled(False)
            except RuntimeError:
                # Handle case where buttons might be deleted
                pass

    def toggle_landmarks(self):
        self.game.show_landmarks = not self.game.show_landmarks
        
    def reset_game(self):
        """Handle reset button click"""
        if self.game.game_completed:
            self.game.reset_game()
            self.game.game_state = self.game.MENU
            self.start_btn.setEnabled(True)
            self.reset_btn.setEnabled(False)

    def closeEvent(self, event):
        self.is_closing = True  # Set closing flag
        if hasattr(self, 'timer'):
            self.timer.stop()  # Stop the timer
        self.game.cleanup()  # Cleanup game resources
        event.accept()
