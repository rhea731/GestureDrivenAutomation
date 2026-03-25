import cv2
import mediapipe as mp
import time
import numpy as np
import json
import tensorflow as tf
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- 1. NEW: LOAD THE GESTURE BRAIN ---
gesture_model = tf.keras.models.load_model('asl_gesture_model.h5')
with open('labels.json', 'r') as f:
    label_names = json.load(f)
# --- NEW: LOAD GESTURE DISPLAY MAPPING ---
with open('gesture_display.json', 'r') as f:
    gesture_display = json.load(f)
# ----------------------------------------

# Helper to calculate distances (same logic used in training)
def get_distances(landmarks):
    dist_list = []
    for i in range(len(landmarks)):
        for j in range(i + 1, len(landmarks)):
            # Euclidean distance: sqrt((x2-x1)^2 + (y2-y1)^2)
            d = np.sqrt((landmarks[i].x - landmarks[j].x)**2 + 
                        (landmarks[i].y - landmarks[j].y)**2)
            dist_list.append(d)
    return np.array(dist_list).reshape(1, -1)

# --- 2. SETUP THE MEDIAPIPE BRAIN ---
model_path = 'hand_landmarker.task'
BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1, # Keeping it to 1 for simpler prediction
    min_hand_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8),
    (9, 10), (10, 11), (11, 12), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20), (5, 9), (9, 13), (13, 17)
]

cap = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame_timestamp_ms = int(time.time() * 1000)

        result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                # --- 3. NEW: PREDICT THE GESTURE ---
                distances = get_distances(hand_landmarks)
                prediction = gesture_model.predict(distances, verbose=0)
                class_id = np.argmax(prediction)
                gesture_name = label_names[class_id]
                confidence = np.max(prediction)

                # --- NEW: GET DISPLAY TEXT ---
                gesture_text = gesture_display.get(gesture_name, gesture_name)
                # ---------------------------

                # Display the prediction
                cv2.putText(frame, f"{gesture_text} ({int(confidence*100)}%)", 
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Draw the skeleton (your original drawing code)
                for connection in HAND_CONNECTIONS:
                    start_pt = (int(hand_landmarks[connection[0]].x * w), int(hand_landmarks[connection[0]].y * h))
                    end_pt = (int(hand_landmarks[connection[1]].x * w), int(hand_landmarks[connection[1]].y * h))
                    cv2.line(frame, start_pt, end_pt, (255, 0, 0), 2)

        cv2.imshow('Hand Gesture Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()