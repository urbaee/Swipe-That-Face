from PyQt6.QtWidgets import QApplication
from gui import launch_camera_selector
from qtgame import GameWindow
import sys

def main():
    app = QApplication(sys.argv)
    cam_index = launch_camera_selector()
    if cam_index is not None:
        window = GameWindow(cam_index)
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
