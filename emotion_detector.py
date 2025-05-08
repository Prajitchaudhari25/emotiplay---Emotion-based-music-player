import cv2
import numpy as np
from deepface import DeepFace
import time

class EmotionDetector:
    def __init__(self):
        # Initialize face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.last_emotion = "neutral"
        self.last_detection_time = time.time()
        self.emotion_stability_threshold = 3  # seconds to keep the same emotion
        
    def detect_emotion(self, frame):
        """Detect emotion from a video frame."""
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # If no face detected, return last emotion
            if len(faces) == 0:
                return self.last_emotion, None
            
            # Process the first face only
            x, y, w, h = faces[0]
            
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Create face region of interest
            face_roi = frame[y:y+h, x:x+w]
            
            # Analyze emotion using DeepFace
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
            
            # Get dominant emotion
            emotion = result[0]['dominant_emotion']
            
            # Implement stability in emotion detection
            current_time = time.time()
            if emotion != self.last_emotion:
                if current_time - self.last_detection_time > self.emotion_stability_threshold:
                    self.last_emotion = emotion
                    self.last_detection_time = current_time
            else:
                self.last_detection_time = current_time
                
            return self.last_emotion, frame
        
        except Exception as e:
            print(f"Error in emotion detection: {str(e)}")
            return self.last_emotion, frame