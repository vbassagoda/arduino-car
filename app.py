import socket
from flask import Flask, render_template, request, jsonify

# Arduino’s IP address (from Arduino Serial Monitor)
HOST_ARDUINO = "172.20.10.2"  # Use Your Arduino's IP. It will print when
                        #You Run the Arduino Server Program
PORT = 12345            # Must match Arduino’s UDP port

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    """Display the control buttons"""
    return render_template('index.html')

@app.route('/direction', methods=['POST'])
def direction():
    """Handle direction button clicks"""
    data = request.get_json()
    direction = data.get('direction', '').upper()
    
    if direction in ['L', 'R', 'F', 'B']:
        print(f"Direction selected: {direction}")
        print(type(direction))
    
        # Create a UDP socket
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mySocket.settimeout(5.0)  # 5 seconds timeout for responses
        print("UDP Client started. Enter a direction (L, R, F)")

        # Send the direction to the server
        sendDirection=direction.encode()
        print('Sending '+str(sendDirection)+' to HOST',HOST_ARDUINO,PORT)
        mySocket.sendto(sendDirection, (HOST_ARDUINO, PORT))
        print('Sent '+direction+' to HOST',HOST_ARDUINO,PORT)

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

        return jsonify({'success': True, 'message': f"Selected: {direction}"})
    else:
        return jsonify({'success': False, 'message': "Invalid direction"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
