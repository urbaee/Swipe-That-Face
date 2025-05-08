import sys
from PyQt6 import QtWidgets
from Video.threads import VideoThread

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Create and start video thread
    video_thread = VideoThread()
    video_thread.start()
    
    # Run the application
    ret = app.exec()
    
    # Cleanup
    video_thread.stop()
    sys.exit(ret)