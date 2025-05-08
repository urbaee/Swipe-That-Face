import cv2
import mediapipe as mp

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        """Initialize the face detector"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=min_detection_confidence
        )

    def detect_faces(self, image):
        """Detect faces in the image"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.face_detection.process(image_rgb)

    def draw_detections(self, image, detections):
        """Draw face detections on the image"""
        if not detections:
            return image

        for detection in detections:
            bbox = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            x, y = int(bbox.xmin * iw), int(bbox.ymin * ih)
            w, h = int(bbox.width * iw), int(bbox.height * ih)

            # Draw bounding box
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw confidence score
            confidence = int(detection.score[0] * 100)
            cv2.putText(image, f'{confidence}%', 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.8, (0, 255, 0), 2)

        return image

class VideoCamera:
    def __init__(self, camera_id=0):
        """Initialize the video camera"""
        self.cap = cv2.VideoCapture(camera_id)

    def read_frame(self):
        """Read a frame from the camera"""
        success, image = self.cap.read()
        return success, image

    def release(self):
        """Release the camera resources"""
        self.cap.release()

def StartDetection():
    # Initialize objects
    detector = FaceDetector()
    camera = VideoCamera()

    while True:
        # Read frame
        success, frame = camera.read_frame()
        if not success:
            print("Failed to capture frame")
            continue

        # Detect faces
        results = detector.detect_faces(frame)

        # Draw detections
        if results.detections:
            frame = detector.draw_detections(frame, results.detections)

        # Display the result
        cv2.imshow('Face Detection', frame)

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    camera.release()
    cv2.destroyAllWindows()

