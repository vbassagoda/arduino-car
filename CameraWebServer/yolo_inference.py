# Process images from the ESP32-CAM with openCV 
import cv2
import numpy as np
from ultralytics import YOLO  # For YOLOv8
import urllib.request
import time

#---------test with the real camera-------------------

CAMERA_IP = "172.20.10.3"  # Replace with your ESP32-CAM IP
capture_url = f"http://{CAMERA_IP}/capture"  # Single frame capture (port 80)

# Test connection
print(f"Testing connection to {capture_url}...")
try:
    with urllib.request.urlopen(capture_url, timeout=5) as response:
        if response.status == 200:
            print(f"✓ Successfully connected to camera!")
        else:
            print(f"✗ Camera returned status {response.status}")
            exit(1)
except Exception as e:
    print(f"✗ Could not connect: {e}")
    print("Please check that the ESP32 camera is powered on and accessible")
    exit(1)

# Load the YOLOv8 model
print("Loading YOLO model...")
model = YOLO("yolov8n.pt")

# Process frames
frame_count = 0
max_frames = 20

print(f"Processing {max_frames} frames...")
while frame_count < max_frames:
    try:
        # Fetch a new frame from the camera
        with urllib.request.urlopen(capture_url, timeout=2) as response:
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
        print(f"Error fetching frame {frame_count + 1}: {e}")
        break
    
    # Run object detection
    results = model(frame)
    
    # Draw bounding boxes on frame
    annotated_frame = results[0].plot()
    
    # Show frame
    cv2.imshow('YOLO Object Detection', annotated_frame)
    
    frame_count += 1
    print(f"Processed frame {frame_count}/{max_frames}")
    
    # Check for quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quit requested by user")
        break
    
    # Small delay between requests
    time.sleep(0.05)

cv2.destroyAllWindows()
print(f"\nDone! Processed {frame_count} frames total.")
