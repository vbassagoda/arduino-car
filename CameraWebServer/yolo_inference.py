# Process images from the ESP32-CAM with openCV 
import cv2
import numpy as np
from ultralytics import YOLO  # For YOLOv8
import urllib.request
import time

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

def get_object_detection(object_name, max_frames=3, capture_url=capture_url, timeout=5):
    object_detected = False
    frame_count = 0
    print(f"Processing {max_frames} frames...")

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
        #cv2.imshow('YOLO Object Detection', annotated_frame) # Show frame

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

    #cv2.destroyAllWindows()
    print(f"\nDone! Processed {frame_count} frames total.")
    
    return object_detected