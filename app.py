import socket
import os
import json
import shutil
from flask import Flask, render_template, request, jsonify
from CameraWebServer.yolo_inference import get_object_detection

# Arduino's IP address (from Arduino Serial Monitor)
HOST_ARDUINO = "172.20.10.2"  # Use Your Arduino's IP. It will print when
                        #You Run the Arduino Server Program
PORT_DIRECTION = 12345            # Must match Arduino's UDP port for direction

# ESP32-CAM IP address (from Serial Monitor after uploading CameraWebServer)
HOST_CAMERA = "172.20.10.3"  # Update with your ESP32-CAM's IP
CAMERA_STREAM_URL = f"http://{HOST_CAMERA}:81/stream"

# Flask app
app = Flask(__name__)

stop_distance = 40

@app.route('/')
def index():
    """Display the control interface"""
    return render_template('index.html', camera_url=CAMERA_STREAM_URL)

def send_direction_to_arduino(direction, speed):
    """Send direction command to Arduino via UDP.
    Returns (direction, speed, distance) on success, or (None, None, None) on failure.
    """
    direction = direction.upper()
    
    if direction not in ["L", "R", "F", "B"]:
        return None, None, None

    else:
        print(f"Direction: {direction}, Speed: {speed}%")

        # Create a UDP socket
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.settimeout(5.0)  # 5 seconds timeout for responses

        # Send direction and speed to Arduino (format: "F,75")
        packet = f"{direction},{speed}".encode()
        print(f'Sending {packet} to HOST {HOST_ARDUINO}:{PORT_DIRECTION}')
        mySocket.sendto(packet, (HOST_ARDUINO, PORT_DIRECTION))
        print(f'Sent {direction} at {speed}% to HOST {HOST_ARDUINO}:{PORT_DIRECTION}')

        # Try to get a response, skip on timeout
        try:
            print('Waiting for response from server')
            response, server_address = mySocket.recvfrom(1024)
            print("Server response:", response.decode())
            response_data = json.loads(response.decode())
            return response_data["direction"], response_data["speed"], response_data["distance"]
        except socket.timeout:
            print("No response received from server within 5 seconds")
            return None, None, None
        except json.JSONDecodeError:
            print("Failed to parse JSON response:", response.decode())
            return None, None, None
        finally:
            # Close the socket
            mySocket.close()


@app.route('/direction', methods=['POST'])
def direction():
    """Handle direction button clicks"""
    data = request.get_json()
    direction = data.get('direction', '').upper()
    speed = data.get('speed', 100)  # Default 100% speed
    
    resp_direction, resp_speed, resp_distance = send_direction_to_arduino(direction, speed)
    
    if resp_direction is not None:
        return jsonify({
            'success': True,
            'direction': resp_direction,
            'speed': resp_speed,
            'distance': resp_distance,
        })
    else:
        return jsonify({'success': False, 'message': "Invalid direction"})

@app.route('/self-drive-to-object', methods=['POST'])
def self_drive_to_object():
    """Handle self-driving to object"""
    # Clear all frames from previous search by deleting and recreating the directory
    output_dir = "annotated_frames"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        print(f"Deleted previous annotated_frames directory")
    os.makedirs(output_dir, exist_ok=True)
    
    data = request.get_json()
    object_name = data.get('object_name', '').lower()

    if object_name in ['person', 'tv']:
        print(f"Self driving to object: {object_name}")

        #call yolo_inference.py to get the object detection
        object_detected = False
        turns = 0
        while turns < 15 and object_detected == False:
            object_detected = get_object_detection(object_name, turn=turns)
            if object_detected:
                print(f"object detected: {object_name}") 
                message = f'Found {object_name}'
                while True:
                    object_detected = get_object_detection(object_name, turn=turns)
                    print(f"object detected: {object_name}") 
                    if object_detected:
                        resp_dir, resp_spd, resp_dist = send_direction_to_arduino("F", 40)
                        print(f"Direction: {resp_dir}, Speed: {resp_spd}, Distance: {resp_dist}")

                    else:
                        resp_dir, resp_spd, resp_dist = send_direction_to_arduino("R", 70)
                        print(f"Direction: {resp_dir}, Speed: {resp_spd}, Distance: {resp_dist}")
                       
                    distance = resp_dist if resp_dist is not None else 0 
                    if distance < stop_distance:
                        break
            else:
                print(f"No object detected: {object_name}")
                resp_dir, resp_spd, resp_dist = send_direction_to_arduino("R", 70)
                print(f"Direction: {resp_dir}, Speed: {resp_spd}, Distance: {resp_dist}")
                turns += 1

        if not object_detected:
            message = f'Mission failed: {object_name} not found :('
        return jsonify({
            'success': object_detected,
            'message': message
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid object name: ' + object_name
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
