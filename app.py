import socket
from flask import Flask, render_template, request, jsonify

# Arduino's IP address (from Arduino Serial Monitor)
HOST_ARDUINO = "172.20.10.2"  # Use Your Arduino's IP. It will print when
                        #You Run the Arduino Server Program
PORT = 12345            # Must match Arduino's UDP port

# ESP32-CAM IP address (from Serial Monitor after uploading CameraWebServer)
HOST_CAMERA = "172.20.10.3"  # Update with your ESP32-CAM's IP
CAMERA_STREAM_URL = f"http://{HOST_CAMERA}:81/stream"

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Display the control interface"""
    return render_template('index.html', camera_url=CAMERA_STREAM_URL)

@app.route('/direction', methods=['POST'])
def direction():
    """Handle direction button clicks"""
    data = request.get_json()
    direction = data.get('direction', '').upper()
    speed = data.get('speed', 100)  # Default 100% speed

    if direction in ['L', 'R', 'F', 'B']:
        print(f"Direction: {direction}, Speed: {speed}%")

        # Create a UDP socket
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.settimeout(5.0)  # 5 seconds timeout for responses

        # Send direction and speed to Arduino (format: "F,75")
        packet = f"{direction},{speed}".encode()
        print(f'Sending {packet} to HOST {HOST_ARDUINO}:{PORT}')
        mySocket.sendto(packet, (HOST_ARDUINO, PORT))
        print(f'Sent {direction} at {speed}% to HOST {HOST_ARDUINO}:{PORT}')

        # Try to get a response, skip on timeout
        try:
            print('Waiting for response from server')
            response, server_address = mySocket.recvfrom(1024)
            print("Server response:", response.decode())
        except socket.timeout:
            print("No response received from server within 5 seconds")
        # Close the socket
        mySocket.close()
        print("Socket closed")

        return jsonify({'success': True, 'message': f"Selected: {direction} at {speed}%"})
    else:
        return jsonify({'success': False, 'message': "Invalid direction"})


@app.route('/self-drive-to-object', methods=['POST'])
def self_drive_to_object():
    """Handle self-driving to object"""
    data = request.get_json()
    object_name = data.get('object_name', '').lower()

    if object_name in ['person', 'tv']:
        print(f"Self driving to object: {object_name}")
        return jsonify({
            'success': True,
            'message': f'Self driving to {object_name}'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid object name: ' + object_name
        }), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
