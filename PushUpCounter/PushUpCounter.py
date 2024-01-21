# pushup_counter.py
import cv2
import mediapipe as mp
import numpy as np
import PoseModule

def start_pushup_counter(target_pushups=10):  # Default target is 10 push-ups
    cap = cv2.VideoCapture(0)
    detector = PoseModule.poseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "Fix Form"

    while cap.isOpened():
        ret, img = cap.read()
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # Convert width to int
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Convert height to int

        if not ret:
            print("Failed to grab frame")
            break  # Exit if no frame is grabbed

        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)

        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23, 25)

            per = np.interp(elbow, (90, 160), (0, 100))
            bar = np.interp(elbow, (90, 160), (380, 50))

            if elbow > 160 and shoulder > 40 and hip > 160:
                form = 1

            if form == 1:
                if per == 0:
                    if elbow <= 90 and hip > 160:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = "Fix Form"

                if per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = "Fix Form"

            # Display the current count
            print(count)

            # Check if the target number of push-ups is reached
            if count >= target_pushups:
                print("Target push-ups reached!")
                break

        # Draw the progress bar on the right
        bar_thickness = 20  # You can adjust the thickness of the bar
        bar_length = int(height * 0.75)  # 75% of the height of the frame
        bar_start_x = int(width * 0.95)  # Start at 95% of the width of the frame
        bar_end_x = bar_start_x + bar_thickness
        if form == 1:
            cv2.rectangle(img, (bar_start_x, int(height * 0.1)), (bar_end_x, int(height * 0.1 + bar_length)), (255,255,255), 3)
            cv2.rectangle(img, (bar_start_x, int(bar)), (bar_end_x, int(height * 0.1 + bar_length)), (255,255,255), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (bar_start_x - 100, int(height * 0.1 + bar_length + 60)), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2)

        # Move the push-up counter to the bottom left
        counter_size = 5  # Font size for the counter
        counter_thickness = 5  # Thickness of the font
        counter_text = str(int(count))
        (text_width, text_height), _ = cv2.getTextSize(counter_text, cv2.FONT_HERSHEY_COMPLEX, counter_size, counter_thickness)
        cv2.rectangle(img, (0, int(height - text_height - 20)), (20 + text_width, int(height +20)), (245,247,255), cv2.FILLED)
        cv2.putText(img, counter_text, (10, int(height - 10)), cv2.FONT_HERSHEY_COMPLEX, counter_size, (46, 64, 87), counter_thickness)

        # Feedback - keep it at the top right or move as desired 
        feedback_pos_x = 500  # X coordinate for feedback text
        feedback_pos_y = 40   # Y coordinate for feedback text
        cv2.rectangle(img, (feedback_pos_x, 0), (832, feedback_pos_y +20), (245,247,255), cv2.FILLED)
        cv2.putText(img, feedback, (feedback_pos_x+8, feedback_pos_y+8), cv2.FONT_HERSHEY_COMPLEX, 2, (46, 64, 87), 2)



        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# This allows the script to be imported without running the function immediately
if __name__ == "__main__":
    start_pushup_counter(20)  # Start with a target of 20 push-ups
