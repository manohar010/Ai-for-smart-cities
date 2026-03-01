import cv2
from ultralytics import YOLO
import requests
import time

# Options
VIDEO_PATH = 'campus_video.mp4'  # Replace with 0 for webcam or a video file path
API_URL = "http://localhost:5000/api/crowd"
LOCATION = "Main Gate"
SEND_INTERVAL_SECONDS = 5

# Load the YOLOv8 model (downloads automatically on first run)
model = YOLO('yolov8n.pt') 

def analyze_video():
    """
    Opens a video stream, detects people, counts them, and sends data to backend.
    """
    cap = cv2.VideoCapture(VIDEO_PATH)
    
    if not cap.isOpened():
        print(f"Error: Could not open video source {VIDEO_PATH}")
        return

    last_send_time = time.time()
    
    print("Starting video analysis. Press 'q' to quit.")
    
    while cap.isOpened():
        success, frame = cap.read()
        
        if not success:
            print("Video stream ended or connection lost.")
            break
            
        # Run YOLO inference on the frame
        # We specify classes=[0] to ONLY detect people (class 0 in COCO dataset)
        results = model(frame, classes=[0], verbose=False)
        
        # Get count of people detected in this frame
        person_count = len(results[0].boxes)
        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        # Display the frame and count
        cv2.putText(
            annotated_frame, 
            f'People: {person_count}', 
            (20, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, (0, 255, 0), 2
        )
        
        cv2.imshow("CampusSense AI Vision", annotated_frame)
        
        # Check if it's time to send data to the backend
        current_time = time.time()
        if current_time - last_send_time >= SEND_INTERVAL_SECONDS:
            send_data_to_backend(person_count)
            last_send_time = current_time
            
        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()


def send_data_to_backend(count):
    """
    Sends the detected count to the Node.js backend.
    """
    if count > 80:
        alert_level = "Critical"
    elif count > 50:
        alert_level = "Warning"
    else:
        alert_level = "Normal"
        
    payload = {
        "location": LOCATION,
        "count": count,
        "alertLevel": alert_level
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=3)
        if response.status_code == 201:
            print(f"[{time.strftime('%H:%M:%S')}] Sent data: {payload} - Server OK")
        else:
            print(f"Error submitting data: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to backend: {e}")

if __name__ == "__main__":
    analyze_video()
