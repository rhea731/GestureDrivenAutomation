import os

GESTURE_FILE = os.path.join(os.path.dirname(__file__), "gestures.json")

CAMERA_INDEX = 0
MAX_SEQUENCE_LENGTH = 60
MIN_SEQUENCE_LENGTH = 15
DTW_THRESHOLD = 0.45
GESTURE_COOLDOWN = 1.5
