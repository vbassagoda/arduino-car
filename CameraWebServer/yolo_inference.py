# Process images from the ESP32-CAM with openCV 
import cv2
import numpy as np
from ultralytics import YOLO  # For YOLOv8
import urllib.request
import time
import os

CAMERA_IP = "172.20.10.3"  # Replace with your ESP32-CAM IP
capture_url = f"http://{CAMERA_IP}/capture"  # Single frame capture (port 80)

# Load the YOLOv8 model
print("Loading YOLO model...")
model = YOLO("yolov8n.pt")

def test_camera_connection(capture_url, timeout = 5):
    print(f"Testing connection to {capture_url}...")
    try:
        with urllib.request.urlopen(capture_url, timeout=timeout) as response:
            if response.status == 200:
                print(f"✓ Successfully connected to camera!")
                return True
            else:
                print(f"✗ Camera returned status {response.status}")
                return response.status
    except Exception as e:
        print(f"✗ Could not connect: {e}")
        print("Please check that the ESP32 camera is powered on and accessible")
        return e

def get_object_detection(object_name, turn=0, max_frames=3, capture_url=capture_url, timeout=5):
    """
    Detect objects in camera frames and save annotated frames locally.
    
    Args:
        object_name: Name of the object to detect
        turn: Turn number (used in filename)
        max_frames: Maximum number of frames to process
        capture_url: URL to capture frames from
        timeout: Request timeout
    
    Returns:
        bool: True if object was detected, False otherwise
    """
    object_detected = False
    frame_count = 0
    print(f"Processing {max_frames} frames for turn {turn}...")
    
    # Create directory for annotated frames if it doesn't exist
    output_dir = "annotated_frames"
    os.makedirs(output_dir, exist_ok=True)

    while frame_count < max_frames:
        try:
            # Fetch a new frame from the camera
            with urllib.request.urlopen(capture_url, timeout=timeout) as response:
                if response.status == 200:
                    # Read JPEG data
                    img_data = response.read()
                    # Decode JPEG to numpy array
                    img_array = np.frombuffer(img_data, np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    
                    if frame is None:
                        print(f"Failed to decode frame {frame_count + 1}")
                        continue
                else:
                    print(f"HTTP error {response.status}")
                    continue
        except Exception as e:
            frame_count += 1
            print(f"Error fetching frame {frame_count}: {e}")
            continue # continue to the next frame
        
        # Run object detection
        results = model(frame)
        annotated_frame = results[0].plot() # Draw bounding boxes on frame
        
        # Save annotated frame with turn and frame number in filename
        filename = f"turn_{turn}_frame_{frame_count + 1}.jpg"
        filepath = os.path.join(output_dir, filename)
        cv2.imwrite(filepath, annotated_frame)
        print(f"Saved annotated frame: {filepath}")

        # search for the object in the frame
        if len(results[0].boxes) > 0:
            detection_class_ids = results[0].boxes.cls.numpy()
            for detection_class_id in detection_class_ids:
                detection_class = model.names[int(detection_class_id)]
                if detection_class == object_name:
                    object_detected = True
                    break
            if object_detected:
                break

        frame_count += 1
        print(f"Processed frame {frame_count}/{max_frames}")
        
        # Small delay between requests
        time.sleep(0.05)

    print(f"\nDone! Processed {frame_count} frames total.")
    
    return object_detected