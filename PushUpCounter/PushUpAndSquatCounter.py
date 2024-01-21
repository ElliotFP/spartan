# pushup_counter.py
import cv2
import mediapipe as mp
import numpy as np
from PushUpCounter import PoseModule
mp_pose = mp.solutions.pose


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


def rescale_frame(frame, percent=50):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def start_pushup_counter(target_pushups=10):  # Default target is 10 push-ups
    cap = cv2.VideoCapture(1)
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

        # Feedback - keep it at the top right or move as desired rgb(245,247,255) rgb(46,64,87)
        feedback_pos_x = 500  # X coordinate for feedback text
        feedback_pos_y = 40   # Y coordinate for feedback text
        cv2.rectangle(img, (feedback_pos_x, 0), (832, feedback_pos_y +20), (245,247,255), cv2.FILLED)
        cv2.putText(img, feedback, (feedback_pos_x+8, feedback_pos_y+8), cv2.FONT_HERSHEY_COMPLEX, 2, (46, 64, 87), 2)



        cv2.imshow('Pushup counter', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def start_squat_counter():
    cap = cv2.VideoCapture(1)

    # Curl counter variables
    counter = 0
    min_ang = 0
    max_ang = 0
    min_ang_hip = 0
    max_ang_hip = 0
    stage = None

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (640, 480)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('output_video_.mp4', fourcc, 24, size)

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is not None:
                frame_ = rescale_frame(frame, percent=75)

            # Recolor image to RGB
            image = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


                # Get coordinates
                hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)

                angle_knee = calculate_angle(hip, knee, ankle)  # Knee joint angle
                angle_knee = round(angle_knee, 2)

                angle_hip = calculate_angle(shoulder, hip, knee)
                angle_hip = round(angle_hip, 2)

                hip_angle = 180 - angle_hip
                knee_angle = 180 - angle_knee

                angle_min.append(angle_knee)
                angle_min_hip.append(angle_hip)

                # print(angle_knee)
                # Visualize angle
                """cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )"""

                cv2.putText(image, str(angle_knee),
                            tuple(np.multiply(knee, [1500, 800]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                cv2.putText(image, str(angle_hip),
                            tuple(np.multiply(hip, [1500, 800]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # Curl counter logic
                if angle_knee > 169:
                    stage = "up"
                if angle_knee <= 90 and stage == 'up':
                    stage = "down"
                    counter += 1
                    print(counter)
                    min_ang = min(angle_min)
                    max_ang = max(angle_min)

                    min_ang_hip = min(angle_min_hip)
                    max_ang_hip = max(angle_min_hip)

                    print(min(angle_min), " _ ", max(angle_min))
                    print(min(angle_min_hip), " _ ", max(angle_min_hip))
                    angle_min = []
                    angle_min_hip = []
            except:
                pass

            # Render squat counter
            # Setup status box
            cv2.rectangle(image, (20, 20), (435, 160), (0, 0, 0), -1)

            # Rep data
            """cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)"""
            cv2.putText(image, "Repetition : " + str(counter),
                        (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Stage data
            """cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)"""
            """cv2.putText(image, stage, 
                        (10,120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)"""

            # Knee angle:
            """cv2.putText(image, 'Angle', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)"""
            cv2.putText(image, "Knee-joint angle : " + str(min_ang),
                        (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Hip angle:
            cv2.putText(image, "Hip-joint angle : " + str(min_ang_hip),
                        (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(203, 17, 17), thickness=2, circle_radius=2)
                                      )

            out.write(image)
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                # break

        cap.release()
        out.release()
        cv2.destroyAllWindows()


# This allows the script to be imported without running the function immediately
if __name__ == "__main__":
    #start_pushup_counter(20)  # Start with a target of 20 push-ups
    start_squat_counter()
