# Dance-Coordination-Checker---IS-Internship
# This project helps check the coordination of dance between two dancers with the same choreography and furnishes dynamic graphical plots for visualisation.
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# function to calculate the distance between feet and hands
def calculate_distance(d, e):
    d = np.array(d)
    e = np.array(e)
    dist = np.linalg.norm(d-e) # taking the positive vector distance between the two points (x and y both considered for dist)
    return dist


def start(filename):
    dist_feet = []
    dist_hands = []
    rh_angles = []
    cap = cv2.VideoCapture(filename)

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if ret:

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]

                right_palm = [landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_PINKY.value].y]
                left_palm = [landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_PINKY.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)
                rh_angles.append(angle)
                disth = calculate_distance(right_palm, left_palm)
                dist_hands.append(disth)
                distf = calculate_distance(right_heel, left_heel)
                dist_feet.append(distf)


            except:
                pass


            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            if not ret:
                break

        cap.release()
        cv2.destroyAllWindows()
    return dist_feet, dist_hands, rh_angles
