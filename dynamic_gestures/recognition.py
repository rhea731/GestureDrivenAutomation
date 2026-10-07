import numpy as np

from .config import MIN_SEQUENCE_LENGTH


def dtw_distance(sequence_a, sequence_b):
    a = np.asarray(sequence_a, dtype=np.float32)
    b = np.asarray(sequence_b, dtype=np.float32)

    n = len(a)
    m = len(b)

    if n == 0 or m == 0:
        return float("inf")

    dp = np.full((n + 1, m + 1), np.inf, dtype=np.float32)
    dp[0, 0] = 0.0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = np.linalg.norm(a[i - 1] - b[j - 1])
            dp[i, j] = cost + min(
                dp[i - 1, j],
                dp[i, j - 1],
                dp[i - 1, j - 1],
            )

    return dp[n, m] / (n + m)


def recognize_gesture(sequence, gestures):
    if not gestures:
        return None, None

    if len(sequence) < MIN_SEQUENCE_LENGTH:
        return None, None

    best_name = None
    best_distance = float("inf")

    for name, template in gestures.items():
        if len(template) < 5:
            continue

        distance = dtw_distance(sequence, template)

        if distance < best_distance:
            best_distance = distance
            best_name = name

    return best_name, best_distance
