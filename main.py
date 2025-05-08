import sys
from PyQt6 import QtWidgets
from Video.threads import StartDetection
# from ui.main_window import MainWindow

if __name__ == "__main__":
#    app = QtWidgets.QApplication(sys.argv)
#    selector = CameraSelector()
#    if selector.exec() == QtWidgets.QDialog.DialogCode.Accepted:
#        selected_camera = selector.get_selected_camera()
#        window = MainWindow(camera_index=selected_camera)
#        window.show()
#        sys.exit(app.exec())
    video_thread = StartDetection()
    video_thread.start()