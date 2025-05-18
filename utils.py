import cv2

def list_available_cameras(max_cams=5):
    available = []
    for i in range(max_cams):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available.append(i)
        cap.release()
    return available
