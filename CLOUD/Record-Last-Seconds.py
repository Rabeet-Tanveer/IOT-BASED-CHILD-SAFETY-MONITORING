import cv2
import time

def record_last_15_seconds(output_file):
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Use 0 for the first webcam connected
    
    # Get the frame rate of the webcam
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Create a VideoWriter object to save the video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
    
    # Record video for 15 seconds
    start_time = time.time()
    while (time.time() - start_time) < 15:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    
    # Release video capture and writer objects
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    output_file = "output.avi"  # Change this to your desired filename
    record_last_15_seconds(output_file)
