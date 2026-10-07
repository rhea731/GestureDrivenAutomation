import time

import cv2

from .automation import execute_gesture
from .camera import get_frame_vector, mp_draw, mp_hands, open_camera

from .config import DTW_THRESHOLD, GESTURE_COOLDOWN, MAX_SEQUENCE_LENGTH, MIN_SEQUENCE_LENGTH
from .gesture_store import load_gestures
from .recognition import recognize_gesture
from .ui import draw_header


def run_recognition():
    gestures = load_gestures()
    if not gestures:
        print()
        print("No gestures have been recorded yet.")
        print("Choose option 1 first.")
        return

    print()
    print("================================")
    print("Loaded gestures:")
    print("===============================")

    for name in gestures:
        print(f"  - {name}")

    print()
    print("Starting camera...")
    print("Press ESC to quit.")
    print()

    cap = open_camera()
    if cap is None:
        return

    sequence = []
    last_detection_time = 0
    detected_text = ""
    detected_until = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Could not read camera.")
            break

        frame = cv2.flip(frame, 1)
        vector, result = get_frame_vector(frame)

        if vector is not None:
            sequence.append(vector)

        if len(sequence) > MAX_SEQUENCE_LENGTH:
            sequence.pop(0)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        draw_header(frame, "GESTURE AUTOMATION - CAMERA ON", (0, 255, 0))

        if vector is not None:
            cv2.putText(frame, "Hand detected", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Show your hand", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

        if len(sequence) >= MIN_SEQUENCE_LENGTH:
            name, distance = recognize_gesture(sequence, gestures)

            if name is not None:
                cv2.putText(frame, f"Possible: {name}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 2)
                cv2.putText(frame, f"Distance: {distance:.3f}", (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 0), 2)

                if distance < DTW_THRESHOLD:
                    now = time.time()
                    if now - last_detection_time > GESTURE_COOLDOWN:
                        execute_gesture(name)
                        last_detection_time = now
                        detected_text = f"DETECTED: {name.upper()}"
                        detected_until = now + 1.5
                        sequence = []


        if time.time() < detected_until:
            cv2.rectangle(frame, (10, 190), (500, 245), (0, 150, 0), -1)
            cv2.putText(frame, detected_text, (25, 228), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)


        cv2.putText(frame, "ESC = Quit", (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow("Dynamic Gesture Automation - Camera", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
