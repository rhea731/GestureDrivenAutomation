from .gesture_store import delete_gesture, list_gestures
from .recorder import record_gesture
from .recognition_loop import run_recognition


def main():
    while True:
        print()
        print()
        print("========================================")
        print("      DYNAMIC GESTURE AUTOMATION")
        print("========================================")
        print()
        print("1. Record new gesture")
        print("2. Start gesture recognition")
        print("3. List saved gestures")
        print("4. Delete gesture")
        print("5. Exit")
        print()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print()
            name = input("Enter gesture name: ").strip()

            if not name:
                print("Gesture name cannot be empty.")
                continue

            record_gesture(name)

        elif choice == "2":
            run_recognition()

        elif choice == "3":
            list_gestures()

        elif choice == "4":
            delete_gesture()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")
