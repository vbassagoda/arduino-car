Code for car with 2 servos and 2 motors withan arduino 1 wifi module
We will use a flask app to control the car

Network:
Both arduino and server need to be connected to a phone hotspot or 2.4G wifi

One time setup:
1) download Arduino IDE
2) install dependencies in Arduino IDE: [todo]
3) install requirements.txt dependencies in virtualenv
4) add file secrets.h in the folders CameraWebServer and car_directions:
  #define SSID "[your wifi]"
  #define PASS "[your password]"


Instructions:
1) Connect the laptop to arduino
2) Open car_directions.ino file in the arduino IDE and then upload code. 
3) Get the arduino IP from the arduino serial monitor and copy it into the app.py

4) Disconnect laptop to arduino and connect it to the camera.
5) Open camera_web_server.ino file in the arduino IDE and then upload code. 
6) Get the camera IP from the arduino serial monitor and copy it into the app.py

7) Connect the motor and arduino cables and put the batteries
  - batteries go to ground and to VIN
  - connect the motor controller cables to the Arduino digital PINs. Check car_directions.ino to see which pin numbers to connect.
  - connect the camera to GND and 5V

8) Activate virtualenv and run python app.py
9) Open html interface in browser in 0.0.0.0:5007

Notes:
- Everything must run in the same WiFi network.
- The WiFi must be 2.4 GHz band since Arduino UNO R4 WiFi doesn't support 5.0 GHz. Phone hotspot also works.
- Do not connect the camera to the computer while it is still connected to the Arduino. 
It can't handle the 2 power sources at the same time
- To debug the camera you can go to the IP address of the camera and check the camera UI to see if the camera works. You might need to click "start stream". If it doesnt work try using another browser for both camera and the car UI endpoint
- The camera only handles one stream at the same time, you cant have 2 apps/tools consuming it at the same time. (e.g. the car UI and the camera UI)