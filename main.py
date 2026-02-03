import cv2
import mediapipe as mp

class KinesisAI:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        # Initialize MediaPipe Hands
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
            
            # 1. Flip frame
            frame = cv2.flip(frame, 1)
            
            # 2. Convert BGR to RGB for MediaPipe
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 3. Process the frame
            results = self.hands.process(img_rgb)

            # 4. Draw Landmarks if hand detected
            if results.multi_hand_landmarks:
                for hand_lms in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame, hand_lms, self.mp_hands.HAND_CONNECTIONS
                    )

            cv2.imshow("Kinesis-AI v0.1", frame)
            
            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = KinesisAI()
    app.run()