import socket
from flask import Flask, render_template, request, jsonify

# Arduino’s IP address (from Arduino Serial Monitor)
HOST = "172.20.10.2"  # Use Your Arduino's IP. It will print when
                        #You Run the Arduino Server Program
PORT = 12345            # Must match Arduino’s UDP port

# Create a UDP socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.settimeout(5.0)  # 5 seconds timeout for responses
print("UDP Client started. Enter a direction (L, R, F)")

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
    
    if direction in ['L', 'R', 'F']:
        print(f"Direction selected: {direction}")
        # Send the direction to the server
        sendDirection=direction.encode()
        mySocket.sendto(sendDirection, (HOST, PORT))
        print('Sent '+direction+' to HOST',HOST,PORT)

        # Try to get a response, skip on timeout
        try:
            response, server_address = mySocket.recvfrom(1024)
            print("Server response:", response.decode())
        except socket.timeout:
            print("No response received from server within 5 seconds")

        return jsonify({'success': True, 'message': f"Selected: {direction}"})
    else:
        return jsonify({'success': False, 'message': "Invalid direction"})

# Close the socket
mySocket.close()
print("Socket closed")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
