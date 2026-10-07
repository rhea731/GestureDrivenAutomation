import cv2
import mediapipe as mp
import numpy as np

from .config import CAMERA_INDEX

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6,
)


def open_camera():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print()
        print("ERROR: Could not open camera.")
        print("Make sure your camera is connected and not being")
        print("used exclusively by another application.")
        return None

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    return cap


def landmarks_to_vector(hand_landmarks):
    points = np.array(
        [
            [landmark.x, landmark.y, landmark.z]
            for landmark in hand_landmarks.landmark
        ],
        dtype=np.float32,
    )

    wrist = points[0].copy()
    points -= wrist

    distances = np.linalg.norm(points, axis=1)
    scale = np.max(distances)

    if scale > 0:
        points /= scale

    return points.flatten()


def get_frame_vector(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if not result.multi_hand_landmarks:
        return None, result

    hand = result.multi_hand_landmarks[0]
    vector = landmarks_to_vector(hand)
    return vector, result
