🎯 What This Project Does:
This program:

Tracks your eye movements using your webcam.

Moves your mouse cursor based on iris position.

Detects blinks to perform mouse clicks (like selecting or opening files).

📦 Technologies Used:
Library	Purpose
cv2	Captures video and processes frames
mediapipe	Tracks face and eye landmarks
pyautogui	Controls the mouse cursor and clicks
numpy	Calculates distances and coordinates

⚙️ How It Works:
1. Camera Input
Captures video from your webcam in real-time.

2. Face Mesh Detection
Uses MediaPipe’s Face Mesh model to detect:

Eye position

Iris center (landmark 468)

Eyelid positions to detect blinks

3. Cursor Movement
Maps the iris (eye center) position to your screen coordinates, and moves the mouse there.

4. Blink Detection
Calculates a blink ratio (distance between eyelids).
When the eyes blink (ratio passes a threshold), it simulates a click using pyautogui.click().

📺 Example Use Case:
Accessibility tools for people who can't use their hands.

A cool human-computer interaction demo project.

Can be extended into virtual mouse, game control, or eye-based authentication systems.

▶️ To Run the Code:
Install required libraries:

bash
Copy
Edit
pip install opencv-python mediapipe pyautogui numpy
Run the Python script.

A window will open showing your face.

Move your eyes to move the mouse.

Blink to simulate a click.
