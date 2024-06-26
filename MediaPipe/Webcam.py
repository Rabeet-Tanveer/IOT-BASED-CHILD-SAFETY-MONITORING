import sys
import time

import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Global variables to calculate FPS
COUNTER, FPS = 0, 0
START_TIME = time.time()
DETECTION_RESULT = None

# Visualization parameters
row_size = 50  # pixels
left_margin = 24  # pixels
text_color = (0, 0, 0)  # black
font_size = 1
font_thickness = 1
fps_avg_frame_count = 10  # Define fps_avg_frame_count
overlay_alpha = 0.5
mask_color = (100, 100, 0)  # cyan


def save_result(result, unused_image):
    global FPS, COUNTER, START_TIME, DETECTION_RESULT

    # Calculate the FPS
    if COUNTER % fps_avg_frame_count == 0:
        FPS = fps_avg_frame_count / (time.time() - START_TIME)
        START_TIME = time.time()

    DETECTION_RESULT = result
    COUNTER += 1


def main():
    cap = cv2.VideoCapture("videos/baby_playing.mp4")

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity = 1
    ) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                sys.exit(
                    "ERROR: Unable to read the video file. Please verify the path to your video file."
                )

            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            # Show the FPS
            fps_text = "FPS = {:.1f}".format(FPS)
            text_location = (left_margin, row_size)
            current_frame = image.copy()
            cv2.putText(
                current_frame,
                fps_text,
                text_location,
                cv2.FONT_HERSHEY_DUPLEX,
                font_size,
                text_color,
                font_thickness,
                cv2.LINE_AA,
            )

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    current_frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing_styles.get_default_pose_landmarks_style(),
                )

            cv2.imshow("pose_landmarker", current_frame)

            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
