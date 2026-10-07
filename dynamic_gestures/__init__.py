"""Gesture automation package."""

from .automation import execute_gesture
from .camera import get_frame_vector, landmarks_to_vector, open_camera
from .cli import main
from .gesture_store import delete_gesture, list_gestures, load_gestures, save_gesture
from .recognition import dtw_distance, recognize_gesture
from .recorder import record_gesture
from .recognition_loop import run_recognition
from .ui import draw_header

__all__ = [
    "main",
    "open_camera",
    "landmarks_to_vector",
    "get_frame_vector",
    "save_gesture",
    "load_gestures",
    "list_gestures",
    "delete_gesture",
    "dtw_distance",
    "recognize_gesture",
    "draw_header",
    "record_gesture",
    "run_recognition",
    "execute_gesture",
]
