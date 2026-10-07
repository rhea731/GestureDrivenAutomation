import cv2


def draw_header(frame, title, color=(0, 255, 0)):
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 55), (20, 20, 20), -1)
    cv2.putText(frame, title, (20, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
