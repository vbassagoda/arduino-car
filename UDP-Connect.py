import socket

# Arduino’s IP address (from Arduino Serial Monitor)
HOST = "172.20.10.2"  # Use Your Arduino's IP. It will print when
                        #You Run the Arduino Server Program
PORT = 12345            # Must match Arduino’s UDP port

# Create a UDP socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.settimeout(5.0)  # 5 seconds timeout for responses

print("UDP Client started. Enter a color (or 'quit' to exit).")

while True:
    # Prompt for a color
    #color = input("Enter a color: ").strip()  # Remove whitespace
    color = input("Enter a color: ") 
    if color.lower() == 'quit':  # Exit condition
        break

    # Send the color to the server
    sendColor=color.encode()
    mySocket.sendto(sendColor, (HOST, PORT))
    print('Sent '+color+' to HOST',HOST,PORT)

    # Try to get a response, skip on timeout
    try:
        response, server_address = mySocket.recvfrom(1024)
        print("Server response:", response.decode())
    except socket.timeout:
        print("No response received from server within 5 seconds")

# Close the socket
mySocket.close()
print("Socket closed")