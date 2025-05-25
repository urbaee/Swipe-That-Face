import cv2
import numpy as np
import tkinter as tk
from facedetect import FaceDetector

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

def is_blinking(landmarks, image_width, image_height):
    """Check if user is blinking (either left or right eye)"""
    def get_coord(idx):
        pt = landmarks.landmark[idx]
        return int(pt.x * image_width), int(pt.y * image_height)
    
    # Get eye landmarks
    left_eye_top = get_coord(159)
    left_eye_bottom = get_coord(145)
    right_eye_top = get_coord(386)
    right_eye_bottom = get_coord(374)
    
    # Calculate eye aspect ratios
    left_eye_height = abs(left_eye_top[1] - left_eye_bottom[1])
    right_eye_height = abs(right_eye_top[1] - right_eye_bottom[1])
    
    # Check if either eye is closed (small height indicates closed eye)
    threshold = 5
    return left_eye_height < threshold or right_eye_height < threshold

def is_eyes_closed(landmarks, image_width, image_height):
    """Check if both eyes are closed"""
    def get_coord(idx):
        pt = landmarks.landmark[idx]
        return int(pt.x * image_width), int(pt.y * image_height)
    
    # Get eye landmarks for both eyes
    left_eye_top = get_coord(159)
    left_eye_bottom = get_coord(145)
    right_eye_top = get_coord(386)
    right_eye_bottom = get_coord(374)
    
    # Calculate eye heights
    left_eye_height = abs(left_eye_top[1] - left_eye_bottom[1])
    right_eye_height = abs(right_eye_top[1] - right_eye_bottom[1])
    
    # Both eyes must be closed (small height)
    threshold = 5
    return left_eye_height < threshold and right_eye_height < threshold

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

def show_expression_game(cam_index: int, emoji_path: str):
    from game import ExpressionGame
    game = ExpressionGame(cam_index)
    game.run()
