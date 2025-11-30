# Process images from the MJPEG stream of theESP32-CAM with openCV 
import cv2
import numpy as np
from ultralytics import YOLO  # For YOLOv8

#---------test with the real camera-------------------

CAMERA_IP = "172.20.10.3"  # Replace with your ESP32-CAM IP
stream_url = f"http://{CAMERA_IP}/capture" # MJPEG stream URL

# Open the stream
cap = cv2.VideoCapture(stream_url)

#---------test with local video file--------------------
# video_path = "video_test.MP4"
# cap = cv2.VideoCapture(video_path)
#-----------------------------------------------------

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Process the frames
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Run object detection
    results = model(frame)
    
    # Draw bounding boxes on frame
    annotated_frame = results[0].plot()
    
    cv2.imshow('YOLO Object Detection', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
