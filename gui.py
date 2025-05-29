import tkinter as tk
from tkinter import ttk
import cv2
from facedetect import FaceDetector
from utils import list_available_cameras
from expression import show_expression_game

def run_landmark_view(cam_index):
    cap = cv2.VideoCapture(cam_index)
    detector = FaceDetector()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Gagal ambil frame.")
            break

        landmarks = detector.get_landmarks(frame)
        if landmarks:
            detector.draw_landmarks(frame, landmarks)

        cv2.imshow(f'Face Landmark Viewer - Camera {cam_index}', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def get_available_cameras():
    """Deteksi kamera yang benar-benar tersedia"""
    available_cameras = []
    max_test = 10  # Test sampai index 10
    
    for i in range(max_test):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # Gunakan DirectShow
        if cap.isOpened():
            # Ambil informasi kamera
            ret, frame = cap.read()
            if ret:
                # Dapatkan nama device
                name = f"Camera {i}"
                try:
                    # Coba dapatkan nama backend
                    backend = cap.getBackendName()
                    if backend:
                        name = f"{backend} Camera {i}"
                except:
                    pass
                available_cameras.append((i, name))
            cap.release()
    return available_cameras

class CameraSelector(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_camera = None
        self.camera_indices = []
        self.initUI()
        
    def initUI(self):
        self.title('Select Camera')
        self.geometry('800x600')  # Ukuran window lebih besar
        self.resizable(False, False)
        
        # Style untuk judul
        title_label = tk.Label(
            self, 
            text="Select Your Camera",
            font=('Arial', 24, 'bold'),  # Font lebih besar
            pady=20
        )
        title_label.pack(pady=40)  # Spacing lebih besar
        
        # Detect available cameras
        cameras = get_available_cameras()
        
        if not cameras:
            label = tk.Label(
                self, 
                text="No cameras found!",
                font=('Arial', 16),  # Font lebih besar
                fg='red'
            )
            label.pack(pady=30)
        else:
            # Store camera indices and names
            self.camera_indices = [idx for idx, name in cameras]
            camera_names = [name for idx, name in cameras]
            
            # Style combobox
            style = ttk.Style()
            style.configure('Custom.TCombobox', font=('Arial', 14))  # Font lebih besar
            
            self.combo = ttk.Combobox(
                self, 
                values=camera_names, 
                state='readonly', 
                width=40,  # Width lebih besar
                font=('Arial', 14),  # Font lebih besar
                style='Custom.TCombobox'
            )
            self.combo.pack(pady=(30, 20))  # Spacing lebih besar
            self.combo.current(0)
            
            # Style button
            select_btn = ttk.Button(
                self, 
                text='Start Camera',  # Text lebih deskriptif
                command=self.on_select,
                style='Custom.TButton'
            )
            
            # Custom style untuk button
            style.configure(
                'Custom.TButton',
                font=('Arial', 14, 'bold'),  # Font lebih besar
                padding=10
            )
            
            select_btn.pack(pady=30)  # Spacing lebih besar

    def on_select(self):
        current_idx = self.combo.current()  # Use current() instead of currentIndex()
        self.selected_camera = self.camera_indices[current_idx]  # Get the actual camera index
        self.destroy()

def launch_camera_selector():
    dialog = CameraSelector()
    dialog.grab_set()  # Make the dialog modal
    dialog.wait_window()  # Wait for the dialog to close
    return dialog.selected_camera if dialog.selected_camera is not None else -1

def main():
    cam_index = launch_camera_selector()
    if cam_index != -1:
        run_landmark_view(cam_index)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    main()
