import cv2
from facedetect import FaceDetector
from expression import is_smiling, is_big_smiling, is_blinking, is_eyes_closed
from playsound import playsound
import threading

class ExpressionGame:
    def __init__(self, cam_index):
        self.cap = cv2.VideoCapture(cam_index)
        self.detector = FaceDetector()
        self.window_size = (640, 640)
        self.setup_window()
        self.setup_game_states()
        self.load_expressions()
        self.success_sound = "sound/good-job.mp3"
        
    def setup_window(self):
        cv2.namedWindow('Swipe That Face!', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Swipe That Face!', *self.window_size)
        
    def setup_game_states(self):
        self.MENU = 0
        self.COUNTDOWN = 1
        self.PLAYING = 2
        self.game_state = self.MENU
        self.countdown_start = None
        self.countdown_duration = 1.0
        self.win_start_time = None
        self.WIN_DURATION = 3
        self.game_completed = False
        self.current_expression = 0
        
    def load_expressions(self):
        self.expressions = [
            {"emoji": "Assets/senyum.png", "detector": is_smiling},
            {"emoji": "Assets/senyumlebar.png", "detector": is_big_smiling},
            {"emoji": "Assets/kedip.png", "detector": is_blinking},
            {"emoji": "Assets/merem.png", "detector": is_eyes_closed},
        ]
        self.current_emoji = cv2.imread(self.expressions[0]["emoji"], cv2.IMREAD_UNCHANGED)
        if self.current_emoji is None:
            raise FileNotFoundError("Emoji image not found!")
        self.current_emoji = cv2.resize(self.current_emoji, (150, 150))

    def reset_game(self):
        self.current_expression = 0
        self.win_start_time = None
        self.game_completed = False
        self.current_emoji = cv2.imread(self.expressions[0]["emoji"], cv2.IMREAD_UNCHANGED)
        self.current_emoji = cv2.resize(self.current_emoji, (150, 150))

    def draw_ui(self, frame, text, position, font_scale=1.2, color=(0, 255, 0)):
        h, w = frame.shape[:2]
        font = cv2.FONT_HERSHEY_DUPLEX
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        
        if position == 'center':
            text_x = (w - text_size[0]) // 2
            text_y = (h + text_size[1]) // 2
        elif position == 'top':
            text_x = (w - text_size[0]) // 2
            text_y = 50
        elif position == 'bottom':
            text_x = (w - text_size[0]) // 2
            text_y = h - 50
            
        cv2.putText(frame, text, (text_x+2, text_y+2), font, font_scale, (0, 0, 0), thickness+1)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

    def show_main_menu(self, frame):
        self.draw_ui(frame, "Swipe That Face!", 'top', 1.5, (0, 255, 0))
        self.draw_ui(frame, "Press SPACE to PLAY", position='center', font_scale=1.0, color=(255, 255, 255))

    def show_countdown(self, frame, number):
        self.draw_ui(frame, str(number), 'center', 4.0, (0, 255, 255))

    def overlay_emoji(self, frame, emoji, pos):
        x, y = pos
        h, w = emoji.shape[:2]
        if emoji.shape[2] == 4:
            alpha = emoji[:, :, 3] / 255.0
            for c in range(3):
                frame[y:y+h, x:x+w, c] = (
                    alpha * emoji[:, :, c] +
                    (1 - alpha) * frame[y:y+h, x:x+w, c]
                )
        else:
            frame[y:y+h, x:x+w] = emoji

    def run(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break

            # Resize frame to square
            h, w = frame.shape[:2]
            size = min(h, w)
            start_x = (w - size) // 2
            start_y = (h - size) // 2
            frame = frame[start_y:start_y+size, start_x:start_x+size]
            frame = cv2.resize(frame, self.window_size)

            if self.game_state == self.MENU:
                self.show_main_menu(frame)
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    self.game_state = self.COUNTDOWN
                    self.countdown_start = cv2.getTickCount()

            elif self.game_state == self.COUNTDOWN:
                current_time = cv2.getTickCount()
                elapsed = (current_time - self.countdown_start) / cv2.getTickFrequency()
                countdown_number = 3 - int(elapsed)
                
                if countdown_number > 0:
                    self.show_countdown(frame, countdown_number)
                else:
                    self.game_state = self.PLAYING
                    self.reset_game()

            elif self.game_state == self.PLAYING:
                self.handle_gameplay(frame)

            cv2.imshow('Swipe That Face!', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r') and self.game_completed:
                if self.game_state == self.PLAYING:
                    self.reset_game()
                else:
                    self.game_state = self.MENU

        self.cap.release()
        cv2.destroyAllWindows()

    def play_success_sound(self):
        # Play in separate thread to avoid blocking
        threading.Thread(target=playsound, args=(self.success_sound,), daemon=True).start()

    def handle_gameplay(self, frame):
        h, w = frame.shape[:2]
        landmarks_list = self.detector.get_landmarks(frame)
        
        self.draw_ui(frame, "Swipe That Face!", 'top')

        if landmarks_list:
            self.detector.draw_landmarks(frame, landmarks_list)
            
            if not self.game_completed:
                expression_detected = self.expressions[self.current_expression]["detector"](
                    landmarks_list[0], w, h)
                if expression_detected and self.win_start_time is None:
                    self.win_start_time = cv2.getTickCount()

        self.handle_win_state(frame)
        
        if not self.game_completed:
            self.overlay_emoji(frame, self.current_emoji, (10, 10))
        else:
            # Show reset instruction when game is completed
            self.draw_ui(frame, "Press R to RESET", position='bottom', font_scale=1.0, color=(255, 255, 255))

    def handle_win_state(self, frame):
        if self.win_start_time is not None and not self.game_completed:
            current_time = cv2.getTickCount()
            elapsed = (current_time - self.win_start_time) / cv2.getTickFrequency()
            
            if elapsed <= self.WIN_DURATION:
                self.draw_ui(frame, "Kamu berhasil!", 'center')
                # Play sound when first entering win state
                if elapsed < 0.1:  # Only play once at the start of win state
                    self.play_success_sound()
            else:
                if self.current_expression < len(self.expressions) - 1:
                    self.current_expression += 1
                    self.current_emoji = cv2.imread(
                        self.expressions[self.current_expression]["emoji"], 
                        cv2.IMREAD_UNCHANGED
                    )
                    self.current_emoji = cv2.resize(self.current_emoji, (150, 150))
                else:
                    self.game_completed = True
                self.win_start_time = None
