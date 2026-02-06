import cv2
import mediapipe as mp
import math
import numpy as np
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
        
        # --- Custom Drawing Styles (Sci-Fi Look) ---
        self.landmark_style = self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=3)
        self.connection_style = self.mp_draw.DrawingSpec(color=(255, 0, 255), thickness=2)

        # --- Audio Setup (PyCaw) ---
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        vol_range = self.volume.GetVolumeRange()
        self.min_vol = vol_range[0]
        self.max_vol = vol_range[1]
        
        # Smoothing Variables
        self.vol = 0
        self.smooth_factor = 0.1

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
                    
                    # 1. Draw Sci-Fi Skeleton
                    self.mp_draw.draw_landmarks(
                        frame, hand_lms, self.mp_hands.HAND_CONNECTIONS,
                        self.landmark_style, self.connection_style
                    )

                    # 2. Control Logic (RIGHT Hand Only)
                    if 'Right' in lbl:
                        # Points
                        x1, y1 = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
                        x2, y2 = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        
                        # Line & Circles
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
                        cv2.circle(frame, (x1, y1), 7, (0, 255, 255), cv2.FILLED)
                        cv2.circle(frame, (x2, y2), 7, (0, 255, 255), cv2.FILLED)
                        cv2.circle(frame, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

                        # Math
                        length = math.hypot(x2 - x1, y2 - y1)
                        
                        # Ranges
                        # Distance Range: 30 (closed) to 200 (open)
                        # Volume Range: min_vol to max_vol
                        # Visual Angle Range: 0 to 360 degrees
                        
                        target_vol = np.interp(length, [30, 200], [self.min_vol, self.max_vol])
                        vol_bar = np.interp(length, [30, 200], [400, 150]) # Keep for reference if needed
                        vol_per = np.interp(length, [30, 200], [0, 100]) # Percentage 0-100
                        angle = np.interp(length, [30, 200], [0, 360])   # Angle 0-360
                        
                        # Smoothness
                        self.vol = self.vol + self.smooth_factor * (target_vol - self.vol)
                        self.volume.SetMasterVolumeLevel(self.vol, None)
                        
                        # --- 3. HUD ARC VISUALS (The Iron Man Look) ---
                        # Draw faint background ring
                        cv2.ellipse(frame, (cx, cy), (60, 60), 0, 0, 360, (50, 50, 50), 3)
                        
                        # Draw active volume arc
                        # Color changes based on volume (Green -> Yellow -> Red look) not implemented yet, using Cyan.
                        cv2.ellipse(frame, (cx, cy), (60, 60), 0, 0, angle, (0, 255, 255), 5)
                        
                        # Display Percentage in the center
                        cv2.putText(frame, f'{int(vol_per)}%', (cx - 20, cy + 5), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

                        if length < 30:
                            cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

            cv2.imshow("Kinesis-AI v0.2 Beta", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = KinesisAI()
    app.run()