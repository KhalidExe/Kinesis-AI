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
        # Joints (Cyan dots)
        self.landmark_style = self.mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=3)
        # Bones (Magenta lines)
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
                    # Check Hand Label
                    lbl = results.multi_handedness[idx].classification[0].label
                    
                    # 1. Draw the cool Sci-Fi Skeleton on ALL hands
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_lms, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.landmark_style, 
                        self.connection_style
                    )

                    # 2. Volume Control Logic (RIGHT Hand Only)
                    if 'Right' in lbl:
                        # Target Points: Thumb (4) and Index (8)
                        x1, y1 = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
                        x2, y2 = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        
                        # Highlight control fingers slightly bigger
                        cv2.circle(frame, (x1, y1), 7, (0, 255, 255), cv2.FILLED)
                        cv2.circle(frame, (x2, y2), 7, (0, 255, 255), cv2.FILLED)
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)

                        # Calculate Distance
                        length = math.hypot(x2 - x1, y2 - y1)

                        # Interpolate Volume (Range: 30 - 200)
                        target_vol = np.interp(length, [30, 200], [self.min_vol, self.max_vol])
                        
                        # Smooth Volume Transition
                        self.vol = self.vol + self.smooth_factor * (target_vol - self.vol)
                        
                        # Send to System
                        self.volume.SetMasterVolumeLevel(self.vol, None)
                        
                        # Visual Feedback for "Click" (Mute/Low)
                        if length < 30:
                            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            cv2.imshow("Kinesis-AI v0.2 Beta", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = KinesisAI()
    app.run()