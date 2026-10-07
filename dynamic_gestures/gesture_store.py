import json
import os

import numpy as np

from .config import GESTURE_FILE


def save_gesture(name, sequence):
    gestures = {}

    if os.path.exists(GESTURE_FILE):
        try:
            with open(GESTURE_FILE, "r") as file:
                gestures = json.load(file)
        except Exception:
            print("Warning: gestures.json could not be read.")
            gestures = {}

    gestures[name] = np.asarray(sequence, dtype=np.float32).tolist()

    with open(GESTURE_FILE, "w") as file:
        json.dump(gestures, file)

    print()
    print("--------------------------------")
    print(f"Gesture saved: {name}")
    print(f"Frames saved: {len(sequence)}")
    print("--------------------------------")


def load_gestures():
    if not os.path.exists(GESTURE_FILE):
        return {}

    try:
        with open(GESTURE_FILE, "r") as file:
            data = json.load(file)
    except Exception:
        print("ERROR: Could not read gestures.json")
        return {}

    gestures = {}
    for name, sequence in data.items():
        gestures[name] = np.asarray(sequence, dtype=np.float32)

    return gestures


def list_gestures():
    gestures = load_gestures()

    print()
    print("================================")
    print("Saved Gestures")
    print("================================")

    if not gestures:
        print("No gestures saved.")
        return

    for name, sequence in gestures.items():
        print(f"- {name}: {len(sequence)} frames")


def delete_gesture():
    gestures = load_gestures()

    if not gestures:
        print("No gestures to delete.")
        return

    print()
    print("Saved gestures:")

    names = list(gestures.keys())

    for i, name in enumerate(names):
        print(f"{i + 1}. {name}")

    choice = input("Enter number to delete: ").strip()

    try:
        index = int(choice) - 1

        if index < 0 or index >= len(names):
            print("Invalid choice.")
            return

        name = names[index]
        del gestures[name]

        with open(GESTURE_FILE, "w") as file:
            json.dump({key: value.tolist() for key, value in gestures.items()}, file)

        print(f"Deleted gesture: {name}")
    except ValueError:
        print("Please enter a number.")
