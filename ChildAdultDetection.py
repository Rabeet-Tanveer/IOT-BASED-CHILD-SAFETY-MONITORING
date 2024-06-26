import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

mp_pose = mp.solutions.pose


def detect_people(image_path):
    output_image_path = "output_image_landmarks.jpg"
    ret_val = 0
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
    print("Reading input image from:", image_path)
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
            ret_val = 0
        else:
            print("{} person(s) detected in the image.".format(num_people))

            # Draw landmarks on the image
            for landmarks in results.pose_landmarks:
                for landmark in landmarks:
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

            # Save the image with landmarks drawn
            if output_image_path:
                success = cv2.imwrite(output_image_path, image)
                if success == None:
                    print("ERROR: Failed to save the image.")

            # Extract the heights of each person
            if num_people == 2:
                heights = []
                for landmarks in results.pose_landmarks:
                    point_12 = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    point_24 = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

                    # Calculate the Euclidean distance between the points
                    distance = ((point_24.x - point_12.x)**2 + (point_24.y - point_12.y)**2)**0.5
                    heights.append(distance)

                # Compare the heights
                if max(heights) / min(heights) >= 1.3:
                    print("One person is an adult and one person is a child.")
                    ret_val = 2
                else:
                    print("Cannot determine if one person is an adult and one person is a child based on the height difference.")
                    ret_val = 3
            else:
                print("Skipping height comparison as there are not exactly 2 people.")

    detector.close()
    return ret_val

