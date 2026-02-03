import cv2

class KinesisAI:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break
            
            # Flip the frame for a mirror effect
            frame = cv2.flip(frame, 1)qqqqqq

            cv2.imshow("Kinesis-AI v0.1", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = KinesisAI()
    app.run()