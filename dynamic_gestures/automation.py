def execute_gesture(name):
    print()
    print("================================")
    print(f"GESTURE DETECTED: {name}")
    print("================================")

    if name == "wave":
        print(">>> WAVE ACTION TRIGGERED <<<")
    elif name == "thumbs_up":
        print(">>> THUMBS UP ACTION TRIGGERED <<<")
    elif name == "stop":
        print(">>> STOP ACTION TRIGGERED <<<")
    else:
        print(f">>> Action for '{name}' <<<")
