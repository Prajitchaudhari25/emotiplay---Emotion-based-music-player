Emotion-Based Music Player
An intelligent desktop music player that detects your facial emotion in real-time and plays songs that match your mood. Powered by DeepFace, OpenCV, PyGame, and PyQt.


🧠 Overview
Emotion is at the heart of how we connect with music. This Emotion-Based Music Player offers a seamless way to experience emotionally adaptive audio. By analyzing your facial expression through your webcam using the DeepFace library, it recognizes your current mood and plays music accordingly—automatically selecting songs from your predefined playlists for emotions like happiness, sadness, anger, and more.

🚀 Features
- Real-time facial emotion recognition via webcam
- Uses DeepFace (VGG-Face, Facenet, etc.) for emotion detection—no manual model training needed
- Automatic music playback using PyGame based on detected mood
- Music folder mapping for emotions like Happy, Sad, Angry, Neutral
- PyQt-based GUI for smooth user experience
- Random song shuffling for variety

📌 Technologies Used
- Python 3.8+
- DeepFace
- OpenCV
- PyGame
- PyQt5
- NumPy

📁 Project Structure
emotion-music-player/
├── music/
│   ├── happy/
│   ├── sad/
│   ├── angry/
│   └── neutral/
│
├── src/
│   ├── main.py               # Entry point with GUI + logic
│   ├── emotion_detector.py   # DeepFace + OpenCV integration
│   ├── music_player.py       # PyGame music controls
│   └── gui.ui                # PyQt UI design (optional .ui file)
│
├── assets/                   # Icons, images for GUI
├── requirements.txt
└── README.txt

🔧 Installation
1. Clone the Repository:
   git clone https://github.com/yourusername/emotion-music-player.git
   cd emotion-music-player

2. Install Dependencies:
   pip install -r requirements.txt

3. Run the App:
   python app.py

   (For GUI version, just run the same file if GUI is integrated)

🎮 How to Use
- The webcam opens in a small GUI window.
- The system captures an image and sends it to DeepFace.
- The dominant emotion (Happy, Sad, Angry, Neutral) is returned.
- A random song from the corresponding folder plays using PyGame.

🎧 Music Categorization
Place .mp3 or .wav songs into the corresponding folders:
music/
├── happy/
├── sad/
├── angry/
└── neutral/

⚙️ Customization Options
- Add more emotions if DeepFace supports them
- Customize UI by editing the PyQt .ui file
- Change webcam settings in OpenCV
- Add pause/next buttons in music_player.py

🧠 Emotion Detection
- DeepFace is used to detect emotions directly from webcam images.
- No training or datasets needed!
- Supported emotions include: Happy, Sad, Angry, Surprise, Fear, Disgust, Neutral

You can simplify or merge these into 4 core categories in your code.

🛑 Troubleshooting
- Webcam not opening → Check device/camera permissions
- No emotion detected → Improve lighting and camera positioning
- No music playing → Ensure valid audio files in emotion folders
- GUI not launching → Ensure PyQt5 is installed

🔮 Future Improvements
- Voice-based emotion detection
- Spotify/Youtube integration
- Learn preferences over time
- Mobile version using Kivy or Flutter


🙏 Acknowledgements
- DeepFace for emotion recognition
- OpenCV for vision
- PyGame for music playback
- PyQt for GUI

📄 License
MIT License – Free to use, modify, and distribute.

👤 Author
Prajit Chaudhari
Adit Sriram
Vaibhav Prakash
