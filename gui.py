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

def launch_camera_selector():
    cam_list = list_available_cameras()

    root = tk.Tk()
    root.title("Camera Selector")
    
    # Set window size and position it at center
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Configure styles
    style = ttk.Style()
    style.configure('Custom.TLabel', font=('Poppins', 12))
    style.configure('Custom.TCombobox', font=('Poppins', 10))
    
    # Create main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = ttk.Label(
        header_frame, 
        text="Select Your Camera", 
        style='Custom.TLabel',
        font=('Poppins', 16, 'bold')
    )
    title_label.pack()
    
    # Camera selection section
    selected_cam = tk.IntVar()
    
    cam_label = ttk.Label(
        main_frame, 
        text="Available Cameras:", 
        style='Custom.TLabel'
    )
    cam_label.pack(anchor=tk.W)
    
    cam_dropdown = ttk.Combobox(
        main_frame, 
        values=cam_list, 
        textvariable=selected_cam,
        style='Custom.TCombobox',
        state='readonly',
        width=30
    )
    cam_dropdown.current(0)
    cam_dropdown.pack(pady=(5, 20), fill=tk.X)
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side=tk.BOTTOM, pady=(0, 20))
    
    def on_start():
        root.destroy()
        #run_landmark_view(selected_cam.get())
        show_expression_game (
            cam_index=selected_cam.get(),
            emoji_path="Assets/senyum.png"
        )
        
    start_button = ttk.Button(
        button_frame,
        text="Start Detection 🎥",
        command=on_start,
        style='Custom.TButton',
        padding=10
    )
    start_button.pack(ipadx=20)
    
    # Configure custom button style
    style.configure(
        'Custom.TButton',
        font=('Poppins', 12),
        background='#008000',
        foreground='#008000'
    )
    
    # Make window non-resizable
    root.resizable(False, False)
    
    root.mainloop()
