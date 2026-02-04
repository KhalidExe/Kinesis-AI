import cv2
import mediapipe as mp
import math

class KinesisAI:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

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
                # Loop through both landmarks and handedness (Label)
                for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                    # Get Hand Label (Right/Left)
                    lbl = results.multi_handedness[idx].classification[0].label
                    
                    # Draw Skeleton
                    self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)

                    # Get Coordinates
                    x1, y1 = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
                    x2, y2 = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    
                    # Display Hand Type (Right/Left)
                    cv2.putText(frame, lbl, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

                    # Draw Interaction Points
                    cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                    cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                    cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                    
                    length = math.hypot(x2 - x1, y2 - y1)
                    if length < 50:
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            cv2.imshow("Kinesis-AI v0.1", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = KinesisAI()
    app.run()