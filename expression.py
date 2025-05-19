import cv2
import numpy as np
import tkinter as tk
from facedetect import FaceDetector
import math

tk.Tk().withdraw()  # Hide main tkinter window for popup use

def is_smiling(landmarks, image_width, image_height):
    """Cek apakah user tersenyum berdasarkan FaceMesh landmark."""

    # Ambil titik-titik yang relevan
    def get_coord(idx):
        pt = landmarks.landmark[idx]
        return int(pt.x * image_width), int(pt.y * image_height)

    # Titik penting
    left_corner = get_coord(61)
    right_corner = get_coord(291)
    mid_upper_lip = get_coord(13)
    bottom_lip = get_coord(14)

    # Mulut harus tertutup (opsional tapi penting)
    mouth_open = abs(bottom_lip[1] - mid_upper_lip[1])
    is_mouth_closed = mouth_open < 5

    # Senyum: sudut bibir lebih tinggi dari titik tengah
    left_is_higher = left_corner[1] < mid_upper_lip[1] - 3
    right_is_higher = right_corner[1] < mid_upper_lip[1] - 3
    is_corner_up = left_is_higher and right_is_higher

    return is_mouth_closed and is_corner_up

def is_big_smiling(landmarks, image_width, image_height):
    """Detect big smile by measuring vertical lip distance ratio"""
    def get_coord(idx):
        pt = landmarks.landmark[idx]
        return int(pt.x * image_width), int(pt.y * image_height)

    left_mouth, right_mouth = get_coord(61), get_coord(291)
    top_lip, bottom_lip = get_coord(13), get_coord(14)

    mouth_width = abs(right_mouth[0] - left_mouth[0])
    mouth_height = abs(bottom_lip[1] - top_lip[1])

    smile_ratio = mouth_width / (mouth_height + 1e-5)

    # Big smile = mulut terbuka cukup tinggi, tapi tetap lebar
    return smile_ratio > 1.8 and mouth_height > 20

def show_expression_game(cam_index: int, emoji_path: str):
    def draw_retry_button(frame):
        h, w = frame.shape[:2]
        button_text = "Press 'R' to Retry"
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 0.8
        thickness = 2
        text_size = cv2.getTextSize(button_text, font, font_scale, thickness)[0]
        text_x = w - text_size[0] - 20  # Position on right side
        text_y = h - 20  # Position at bottom
        
        # Draw button text with shadow
        cv2.putText(frame, button_text, (text_x+2, text_y+2), font, font_scale, (0, 0, 0), thickness+1)
        cv2.putText(frame, button_text, (text_x, text_y), font, font_scale, (0, 255, 0), thickness)
        return frame

    cap = cv2.VideoCapture(cam_index)
    detector = FaceDetector()
    
    def reset_game():
        nonlocal current_expression, win_start_time, game_completed, current_emoji
        current_expression = 0
        win_start_time = None
        game_completed = False
        current_emoji = cv2.imread(expressions[0]["emoji"], cv2.IMREAD_UNCHANGED)
        current_emoji = cv2.resize(current_emoji, (150, 150))

    # Initialize game variables
    win_start_time = None
    WIN_DURATION = 3
    game_completed = False
    
    # Expression states
    current_expression = 0
    expressions = [
        {"emoji": "Assets/senyum.png", "detector": is_smiling},
        {"emoji": "Assets/senyumlebar.png", "detector": is_big_smiling}
    ]
    
    # Load first emoji
    current_emoji = cv2.imread(expressions[0]["emoji"], cv2.IMREAD_UNCHANGED)
    if current_emoji is None:
        print("Emoji image not found!")
        return
    current_emoji = cv2.resize(current_emoji, (150, 150))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        h, w = frame.shape[:2]
        landmarks_list = detector.get_landmarks(frame)

        # Draw title
        title = "Swipe That Face!"
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 1.2
        thickness = 2
        text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = 50
        cv2.putText(frame, title, (text_x+2, text_y+2), font, font_scale, (0, 0, 0), thickness+1)
        cv2.putText(frame, title, (text_x, text_y), font, font_scale, (0, 255, 0), thickness)

        # Handle game logic
        if landmarks_list:
            detector.draw_landmarks(frame, landmarks_list)
            
            if not game_completed:
                expression_detected = expressions[current_expression]["detector"](landmarks_list[0], w, h)
                if expression_detected and win_start_time is None:
                    win_start_time = cv2.getTickCount()

        # Handle win state and progression
        if win_start_time is not None and not game_completed:
            current_time = cv2.getTickCount()
            elapsed = (current_time - win_start_time) / cv2.getTickFrequency()
            
            if elapsed <= WIN_DURATION:
                text = "Kamu berhasil!"
                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                text_x = (w - text_size[0]) // 2
                text_y = h // 2
                cv2.putText(frame, text, (text_x+2, text_y+2), font, font_scale, (0, 0, 0), thickness+1)
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 0), thickness)
            else:
                if current_expression < len(expressions) - 1:
                    current_expression += 1
                    current_emoji = cv2.imread(expressions[current_expression]["emoji"], cv2.IMREAD_UNCHANGED)
                    current_emoji = cv2.resize(current_emoji, (150, 150))
                else:
                    game_completed = True
                win_start_time = None

        # Draw current emoji if game is not completed
        if not game_completed:
            overlay_img(frame, current_emoji, (10, 10))
        else:
            # Draw retry button when game is completed
            frame = draw_retry_button(frame)

        cv2.imshow('Tiru Ekspresi Ini 😁', frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and game_completed:
            reset_game()

    cap.release()
    cv2.destroyAllWindows()

def overlay_img(background, overlay, pos):
    """Gabungin overlay (dengan transparansi) ke frame utama."""
    x, y = pos
    h, w = overlay.shape[:2]

    # Cek apakah ada alpha channel
    if overlay.shape[2] == 4:
        alpha = overlay[:, :, 3] / 255.0
        for c in range(3):
            background[y:y+h, x:x+w, c] = (
                alpha * overlay[:, :, c] +
                (1 - alpha) * background[y:y+h, x:x+w, c]
            )
    else:
        background[y:y+h, x:x+w] = overlay
