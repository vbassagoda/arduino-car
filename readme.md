Code for car with 2 servos and 2 motors withan arduino 1 wifi module
We will use a flask app to control the car

Network:
Both arduino and server need to be connected to a phone hotspot or 2.4G wifi


Instructions:
1) add file secrets.h in the folders CameraWebServer and car_directions:
  #define SSID "[your wifi]"
  #define PASS "[your password]"
2) connect the laptop to arduino and upload code
3) run .ino file to get the IP from the arduino serial monitor and copy it into the app.py
4) run python app.py
5) open html interface in browser in 0.0.0.0:5007