import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

mp_pose = mp.solutions.pose

def detect_people(image_path):
    options = vision.PoseLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path='Models/pose_landmarker_lite.task'),
        running_mode=vision.RunningMode.IMAGE,
        num_poses=2,
        min_pose_detection_confidence=0.5,
        min_pose_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_segmentation_masks=False)

    detector = vision.PoseLandmarker.create_from_options(options)

    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("ERROR: Unable to read the image file.")
        return

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

    # Run pose landmarker using the model.
    results = detector.detect(mp_image)

    if results:
        num_people = len(results.pose_landmarks)
        if num_people == 0:
            print("No people detected in the image.")
        elif num_people == 1:
            print("One person detected in the image.")
        elif num_people == 2:
            print("Two people detected in the image.")
        else:
            print("More than two people detected in the image.")

    detector.close()

# Path to the image
image_path = "download.jpg"

# Detect people in the image
detect_people(image_path)
