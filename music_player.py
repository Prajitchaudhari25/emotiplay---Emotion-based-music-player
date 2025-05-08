import os
import random
import pygame
from pygame import mixer

class MusicPlayer:
    def __init__(self, music_dir="music"):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Base directory for music files
        self.music_dir = music_dir
        
        # Dictionary to map emotions to their directories
        self.emotion_dirs = {
            "happy": os.path.join(music_dir, "happy"),
            "sad": os.path.join(music_dir, "sad"),
            "angry": os.path.join(music_dir, "angry"),
            "neutral": os.path.join(music_dir, "neutral"),
            "fear": os.path.join(music_dir, "sad"),      # Map fear to sad
            "disgust": os.path.join(music_dir, "angry"), # Map disgust to angry
            "surprise": os.path.join(music_dir, "happy") # Map surprise to happy
        }
        
        # Current emotion and song
        self.current_emotion = None
        self.current_song = None
        self.is_playing = False
        
        # Create directories if they don't exist
        for emotion_dir in self.emotion_dirs.values():
            os.makedirs(emotion_dir, exist_ok=True)
    
    def get_random_song(self, emotion):
        """Get a random song from the emotion directory."""
        emotion_dir = self.emotion_dirs.get(emotion, self.emotion_dirs["neutral"])
        
        # Get all music files in the directory
        songs = [f for f in os.listdir(emotion_dir) if f.endswith(('.mp3', '.wav'))]
        
        # If no songs available for this emotion, try neutral
        if not songs and emotion != "neutral":
            emotion_dir = self.emotion_dirs["neutral"]
            songs = [f for f in os.listdir(emotion_dir) if f.endswith(('.mp3', '.wav'))]
        
        # If still no songs, return None
        if not songs:
            return None
        
        # Return a random song
        return os.path.join(emotion_dir, random.choice(songs))
    
    def play_for_emotion(self, emotion):
        """Play a song based on the detected emotion."""
        # If same emotion is already playing, do nothing
        if emotion == self.current_emotion and self.is_playing:
            return
        
        # Stop current playback
        if self.is_playing:
            pygame.mixer.music.stop()
        
        # Get a random song for the emotion
        song_path = self.get_random_song(emotion)
        
        # If no song available, do nothing
        if not song_path:
            print(f"No songs available for {emotion}")
            self.is_playing = False
            self.current_emotion = None
            self.current_song = None
            return
        
        # Load and play the song
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.current_emotion = emotion
            self.current_song = os.path.basename(song_path)
            print(f"Now playing: {self.current_song} ({emotion})")
        except Exception as e:
            print(f"Error playing music: {str(e)}")
            self.is_playing = False
    
    def stop(self):
        """Stop music playback."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
    
    def pause(self):
        """Pause music playback."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
    
    def resume(self):
        """Resume music playback."""
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def get_current_song_info(self):
        """Return information about the current song."""
        if self.current_song and self.current_emotion:
            return f"{self.current_song} ({self.current_emotion})"
        return "No song playing"