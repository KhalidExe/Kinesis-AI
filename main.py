import cv2
import mediapipe as mp
import math
import numpy as np
import pyautogui # New for v0.3.0
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class KinesisAI:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
        # --- MediaPipe Setup ---
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Styles
        self.landmark_style = self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=3)
        self.connection_style = self.mp_draw.DrawingSpec(color=(255, 0, 255), thickness=2)

        # --- Audio Setup (Right Hand) ---
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        vol_range = self.volume.GetVolumeRange()
        self.min_vol = vol_range[0]
        self.max_vol = vol_range[1]
        
        # Variables
        self.vol = 0
        self.smooth_factor = 0.1
        self.prev_speed_state = "Normal" # For Left Hand Logic

    def run(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break
            
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            
            h, w, c = frame.shape

            if results.multi_hand_landmarks:
                for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                    lbl = results.multi_handedness[idx].classification[0].label
                    
                    # Draw Skeleton
                    self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS, self.landmark_style, self.connection_style)

                    # Get Key Landmarks
                    # Thumb(4), Index(8), PinkyTip(20), PinkyMCP(17)
                    x4, y4 = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
                    x8, y8 = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
                    
                    # Calculate Pinch Distance
                    length = math.hypot(x8 - x4, y8 - y4)
                    cx, cy = (x4 + x8) // 2, (y4 + y8) // 2

                    # =================================================
                    # 🔊 RIGHT HAND: Smart Volume Control
                    # =================================================
                    if 'Right' in lbl:
                        # --- SMART LOCK CHECK ---
                        # Check if Pinky is folded (Tip y > Knuckle y means finger is DOWN)
                        pinky_tip_y = hand_lms.landmark[20].y
                        pinky_mcp_y = hand_lms.landmark[17].y
                        
                        # Note: In screen coordinates, Y increases downwards.
                        # So if Tip > MCP, the finger is pointing DOWN (Folded).
                        is_pinky_folded = pinky_tip_y > pinky_mcp_y

                        if is_pinky_folded:
                            # ACTIVE MODE: Visual Feedback (Green HUD)
                            status_color = (0, 255, 0)
                            cv2.putText(frame, "VOL: ACTIVE", (x4, y4 - 50), cv2.FONT_HERSHEY_PLAIN, 1, status_color, 2)
                            
                            # Draw Control Lines
                            cv2.line(frame, (x4, y4), (x8, y8), (0, 255, 255), 3)
                            
                            # Volume Logic
                            target_vol = np.interp(length, [30, 200], [self.min_vol, self.max_vol])
                            vol_per = np.interp(length, [30, 200], [0, 100])
                            angle = np.interp(length, [30, 200], [0, 360])
                            
                            self.vol = self.vol + self.smooth_factor * (target_vol - self.vol)
                            self.volume.SetMasterVolumeLevel(self.vol, None)

                            # HUD Arc
                            cv2.ellipse(frame, (cx, cy), (60, 60), 0, 0, 360, (50, 50, 50), 3)
                            cv2.ellipse(frame, (cx, cy), (60, 60), 0, 0, angle, status_color, 5)
                            cv2.putText(frame, f'{int(vol_per)}%', (cx - 20, cy + 5), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                        else:
                            # LOCKED MODE: Visual Feedback (Red/Gray HUD)
                            cv2.putText(frame, "VOL: LOCKED (Fold Pinky)", (x4, y4 - 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
                            # Just draw simple points, no lines, no volume change
                            cv2.circle(frame, (x4, y4), 5, (100, 100, 100), cv2.FILLED)
                            cv2.circle(frame, (x8, y8), 5, (100, 100, 100), cv2.FILLED)

                    # =================================================
                    # ⏩ LEFT HAND: Playback Speed (v0.3.0 Alpha)
                    # =================================================
                    elif 'Left' in lbl:
                        cv2.putText(frame, "Speed Control (Coming Soon)", (x4, y4 - 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                        # Placeholder for next step:
                        # Pinch Close -> Slow Down
                        # Pinch Open -> Speed Up
                        if length < 40:
                             cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                             # pyautogui.press('shift', '<') # Example logic

            cv2.imshow("Kinesis-AI v0.3 Alpha", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = KinesisAI()
    app.run()