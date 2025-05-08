from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QComboBox, QFileDialog)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize
import cv2
import os

class EmotionMusicPlayerUI(QMainWindow):
    update_frame_signal = pyqtSignal(QImage)
    
    def __init__(self, emotion_detector, music_player):
        super().__init__()
        
        # Components
        self.emotion_detector = emotion_detector
        self.music_player = music_player
        
        # Video capture
        self.capture = None
        self.timer = QTimer()
        
        # Initialize UI
        self.init_ui()
        
        # Connect timer to update function
        self.timer.timeout.connect(self.update_frame)
    
    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Emotion-Based Music Player")
        self.setGeometry(100, 100, 800, 600)
        
        # Main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Video feed area
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        
        # Status area
        status_layout = QHBoxLayout()
        
        self.emotion_label = QLabel("Detected Emotion: None")
        self.emotion_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        self.song_label = QLabel("Current Song: None")
        self.song_label.setStyleSheet("font-size: 16px;")
        
        status_layout.addWidget(self.emotion_label)
        status_layout.addWidget(self.song_label)
        
        # Control area
        control_layout = QHBoxLayout()
        
        # Start/Stop Webcam
        self.webcam_btn = QPushButton("Start Webcam")
        self.webcam_btn.clicked.connect(self.toggle_webcam)
        self.webcam_btn.setMinimumSize(QSize(120, 40))
        
        # Emotion selector
        self.emotion_selector = QComboBox()
        self.emotion_selector.addItems(["Auto (Detect)", "Happy", "Sad", "Angry", "Neutral", "Surprise"])
        self.emotion_selector.currentIndexChanged.connect(self.emotion_selection_changed)
        self.emotion_selector.setMinimumSize(QSize(120, 40))
        
        # Music controls
        self.play_pause_btn = QPushButton("Pause")
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.play_pause_btn.setEnabled(False)
        self.play_pause_btn.setMinimumSize(QSize(120, 40))
        
        # Add music button
        self.add_music_btn = QPushButton("Add Music")
        self.add_music_btn.clicked.connect(self.add_music)
        self.add_music_btn.setMinimumSize(QSize(120, 40))
        
        control_layout.addWidget(self.webcam_btn)
        control_layout.addWidget(self.emotion_selector)
        control_layout.addWidget(self.play_pause_btn)
        control_layout.addWidget(self.add_music_btn)
        
        # Add layouts to main layout
        main_layout.addWidget(self.video_label)
        main_layout.addLayout(status_layout)
        main_layout.addLayout(control_layout)
        
        # Set the main layout
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Connect signal to update frame
        self.update_frame_signal.connect(self.set_frame)
    
    def toggle_webcam(self):
        """Start or stop the webcam."""
        if self.timer.isActive():
            # Stop timer and release video capture
            self.timer.stop()
            if self.capture:
                self.capture.release()
                self.capture = None
            
            # Update UI
            self.webcam_btn.setText("Start Webcam")
            self.play_pause_btn.setEnabled(False)
            self.video_label.clear()
            self.video_label.setText("Webcam Off")
        else:
            # Initialize video capture
            self.capture = cv2.VideoCapture(0)
            
            if self.capture.isOpened():
                # Start timer
                self.timer.start(30)  # Update every 30ms (approx. 33 fps)
                
                # Update UI
                self.webcam_btn.setText("Stop Webcam")
                self.play_pause_btn.setEnabled(True)
            else:
                self.video_label.setText("Error: Could not open webcam")
    
    def update_frame(self):
        """Capture and process a frame from the webcam."""
        if self.capture:
            ret, frame = self.capture.read()
            
            if ret:
                # Detect emotion
                if self.emotion_selector.currentText() == "Auto (Detect)":
                    emotion, processed_frame = self.emotion_detector.detect_emotion(frame)
                    
                    # Update emotion label
                    self.emotion_label.setText(f"Detected Emotion: {emotion.capitalize()}")
                    
                    # Play music for emotion
                    self.music_player.play_for_emotion(emotion)
                    
                    # Update song info
                    self.song_label.setText(f"Current Song: {self.music_player.get_current_song_info()}")
                    
                    # Use processed frame if available
                    if processed_frame is not None:
                        frame = processed_frame
                
                # Convert frame to QImage
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # Emit signal to update UI in the main thread
                self.update_frame_signal.emit(q_img)
    
    def set_frame(self, q_img):
        """Set the frame in the UI."""
        # Scale the QImage to fit the video label
        scaled_img = q_img.scaled(self.video_label.width(), self.video_label.height(), 
                                  Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Set the pixmap
        self.video_label.setPixmap(QPixmap.fromImage(scaled_img))
    
    def emotion_selection_changed(self):
        """Handle manual emotion selection."""
        selected = self.emotion_selector.currentText()
        
        if selected != "Auto (Detect)":
            emotion = selected.lower()
            self.emotion_label.setText(f"Selected Emotion: {selected}")
            self.music_player.play_for_emotion(emotion)
            self.song_label.setText(f"Current Song: {self.music_player.get_current_song_info()}")
    
    def toggle_play_pause(self):
        """Toggle between play and pause."""
        if self.music_player.is_playing:
            self.music_player.pause()
            self.play_pause_btn.setText("Resume")
        else:
            self.music_player.resume()
            self.play_pause_btn.setText("Pause")
    
    def add_music(self):
        """Add music files to the appropriate emotion folder."""
        emotion_mapping = {
            "Happy": "happy",
            "Sad": "sad",
            "Angry": "angry",
            "Neutral": "neutral",
            "Surprise": "surprise"
        }
        
        # Select emotion
        emotion_dialog = QComboBox()
        emotion_dialog.addItems(list(emotion_mapping.keys()))
        
        # Get files
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Music Files", "", "Audio Files (*.mp3 *.wav)"
        )
        
        if files:
            # Get selected emotion
            selected_emotion = emotion_dialog.currentText()
            emotion_folder = emotion_mapping.get(selected_emotion, "neutral")
            
            # Copy files to emotion directory
            target_dir = self.music_player.emotion_dirs.get(emotion_folder)
            
            for file_path in files:
                file_name = os.path.basename(file_path)
                target_path = os.path.join(target_dir, file_name)
                
                # Copy file using shutil or similar
                import shutil
                shutil.copy2(file_path, target_path)
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Stop webcam and music
        if self.timer.isActive():
            self.timer.stop()
        
        if self.capture:
            self.capture.release()
        
        self.music_player.stop()
        
        # Accept close event
        event.accept()