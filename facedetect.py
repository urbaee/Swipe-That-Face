import mediapipe as mp
import cv2

class FaceDetector:
    def __init__(self, max_faces=1):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        return results.multi_face_landmarks

    def draw_landmarks(self, frame, landmarks):
        # Draw title text
        ih, iw, _ = frame.shape
        title = "Swipe That Face!"
        font = cv2.FONT_HERSHEY_DUPLEX  # Closest to Poppins available in OpenCV
        font_scale = 1.2
        thickness = 2
        text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]
        text_x = (iw - text_size[0]) // 2  # Center horizontally
        text_y = 50  # Position from top
        
        # Draw text shadow/outline for better visibility
        cv2.putText(frame, title, (text_x+2, text_y+2), font, font_scale, (0, 0, 0), thickness+1)
        cv2.putText(frame, title, (text_x, text_y), font, font_scale, (0, 255, 0), thickness)

        # Draw landmarks
        for face_landmarks in landmarks:
            self.mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mp_drawing.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=1,
                    circle_radius=1
                )
            )
        return frame  # Return the modified frame

