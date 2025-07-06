import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Drawing utils
mp_drawing = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()


# To calculate blinking
def get_blink_ratio(landmarks, indices):
    left = np.array([landmarks[indices[0]].x, landmarks[indices[0]].y])
    right = np.array([landmarks[indices[1]].x, landmarks[indices[1]].y])
    top = np.array([landmarks[indices[2]].x, landmarks[indices[2]].y])
    bottom = np.array([landmarks[indices[3]].x, landmarks[indices[3]].y])

    hor_line = np.linalg.norm(left - right)
    ver_line = np.linalg.norm(top - bottom)

    return hor_line / ver_line


blink_threshold = 4.5
last_click_time = 0
click_delay = 1  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # RGB conversion
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark

        # Eye landmarks (right eye)
        eye_indices = [33, 133, 159, 145]  # [left, right, top, bottom]
        blink_ratio = get_blink_ratio(mesh_points, eye_indices)

        # Iris center for eye tracking
        iris_x = int(mesh_points[468].x * w)
        iris_y = int(mesh_points[468].y * h)

        screen_x = np.interp(iris_x, [0, w], [0, screen_width])
        screen_y = np.interp(iris_y, [0, h], [0, screen_height])

        pyautogui.moveTo(screen_x, screen_y)

        # Blink detection for click
        if blink_ratio > blink_threshold:
            current_time = time.time()
            if current_time - last_click_time > click_delay:
                pyautogui.click()
                last_click_time = current_time
                cv2.putText(frame, "Click", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

        # Draw eye tracking point
        cv2.circle(frame, (iris_x, iris_y), 3, (255, 0, 255), -1)

    cv2.imshow("Eye Cursor Controller", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
