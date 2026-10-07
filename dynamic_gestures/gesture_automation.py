"""Compatibility wrapper for the modular gesture automation package."""

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from dynamic_gestures.cli import main
else:
    from .cli import main


if __name__ == "__main__":
    main()
