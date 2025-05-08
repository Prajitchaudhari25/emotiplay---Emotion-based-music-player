import sys
import os
from PyQt5.QtWidgets import QApplication

from emotion_detector import EmotionDetector
from music_player import MusicPlayer
from ui import EmotionMusicPlayerUI

def main():
    # Create directories for music
    os.makedirs("music/happy", exist_ok=True)
    os.makedirs("music/sad", exist_ok=True)
    os.makedirs("music/angry", exist_ok=True)
    os.makedirs("music/neutral", exist_ok=True)
    os.makedirs("music/surprised", exist_ok=True)
    
    # Initialize components
    app = QApplication(sys.argv)
    
    # Create emotion detector
    emotion_detector = EmotionDetector()
    
    # Create music player
    music_player = MusicPlayer()
    
    # Create UI
    ui = EmotionMusicPlayerUI(emotion_detector, music_player)
    ui.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()