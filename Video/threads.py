import cv2
import mediapipe as mp
from PyQt6.QtCore import QThread, pyqtSignal
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """Initialize MediaPipe face mesh (includes detection internally)"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def process_frame(self, image):
        """Process the image and return landmarks if any"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Add image dimensions
        h, w = image.shape[:2]
        results = self.face_mesh.process(image_rgb)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                face_landmarks.image_dimensions = {'width': w, 'height': h}
        return results

    def draw_landmarks(self, image, mesh_results):
        ih, iw, _ = image.shape
        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                # Draw face mesh
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.drawing_spec
                )

                # Draw bounding box
                x_coords = [landmark.x for landmark in face_landmarks.landmark]
                y_coords = [landmark.y for landmark in face_landmarks.landmark]
                x_min = int(min(x_coords) * iw)
                x_max = int(max(x_coords) * iw)
                y_min = int(min(y_coords) * ih)
                y_max = int(max(y_coords) * ih)
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        return image

class VideoCamera:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        # Set resolution to 1920x1080
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def read_frame(self):
        success, image = self.cap.read()
        if success:
            # Resize frame if it's not in the desired resolution
            if image.shape[1] != 1920 or image.shape[0] != 1080:
                image = cv2.resize(image, (1920, 1080))
        return success, image

    def release(self):
        self.cap.release()

class VideoThread(QThread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        detector = FaceDetector()
        camera = VideoCamera()

        while self.running:
            success, frame = camera.read_frame()
            if not success:
                print("Failed to capture frame")
                continue

            mesh_results = detector.process_frame(frame)
            frame = detector.draw_landmarks(frame, mesh_results)

            cv2.imshow('Face Mesh', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()

    def stop(self):
        self.running = False
        self.wait()

if __name__ == "__main__":
    import sys
    from PyQt6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    video_thread = VideoThread()
    video_thread.start()

    ret = app.exec()

    video_thread.stop()
    sys.exit(ret)
