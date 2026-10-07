import cv2

from .automation import execute_gesture
from .camera import get_frame_vector, mp_draw, mp_hands, open_camera
from .config import GESTURE_COOLDOWN, DTW_THRESHOLD, MAX_SEQUENCE_LENGTH, MIN_SEQUENCE_LENGTH
from .gesture_store import save_gesture
from .recognition import recognize_gesture
from .ui import draw_header


def record_gesture(name):
    cap = open_camera()

    if cap is None:
        return

    sequence = []
    recording = False

    print()
    print("================================")
    print(f"Recording gesture: {name}")
    print("==============================")
    print()
    
    print("Press SPACE to START recording.")
    print("Press SPACE again to STOP.")
    print("Press ESC to cancel.")
    print()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Could not read camera")
            break

        frame = cv2.flip(frame, 1)
        vector, result = get_frame_vector(frame)

        if recording and vector is not None:
            sequence.append(vector)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        if recording:
            draw_header(frame, "RECORDING - Perform your gesture!", (0, 0, 255))
            cv2.circle(frame, (frame.shape[1] - 30, 28), 10, (0, 0, 255), -1)
            cv2.putText(frame, f"Frames: {len(sequence)}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            draw_header(frame, f"Ready to record: {name}", (0, 255, 0))
            cv2.putText(frame, "SPACE = Start recording", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("Gesture Recorder", frame)
        key = cv2.waitKey(1) & 0xFF




        if key == 32:
            if not recording:
                sequence = []
                recording = True
                print("Recording started...")
            else:
                recording = False
                print(f"Recording stopped. {len(sequence)} frames captured.")

                if len(sequence) >= 5:
                    save_gesture(name, sequence)
                else:
                    print("Gesture was too short.")

                break
        elif key == 27:
            print("Recording cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()
