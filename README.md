# Tejas
Bot for Human Detection, Tracking and Obstacle Avoidance for Resonance Hardware Hackathon at KLE Technological University, Dr. M. S. Sheshgiri Campus, Belagavi

Electronic Components Required:
1. Raspberry Pi 4 Model B+
2. HC-SR04 Ultrasonic Sensor
3. L298N Motor Driver
4. Dual shaft DC Motors x 2
5. Raspberry Pi Camera

# Setting up Raspberry Pi
1. Using 'Rasbperry Pi Imager', install Raspberry Pi OS compatible with the Raspberry Pi 4 (Recommended: Raspberry Pi OS (Debian Bullseye) Legacy 32-Bit Full with Desktop environment and recommended applications) onto the SD Card (Recommended: Class 10 32 GB Micro SD Card).
2. Access the Raspberry Pi through Wi-Fi via SSH
3. Set up serial connection and type the following in SSH:
```
sudo raspi-config
```
4. Change the following settings:
   a) Go to interface settings
   b) Enable Legacy camera
   c) Enable SSH
   d) Enable VNC

If you encounter ```Cannot currently show the Desktop```, go to ```sudo nano /boot/config.txt``` and type the following lines after ```#hdmi_safe=1```:
```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=9
```
Save the file and exit the text editor (in ```nano```, you do this by pressing CTRL + X, then Y, and Enter).<br/>
5. Run the following commands:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
sudo apt-get install python-dev
sudo apt-get install python3-opencv
```
6. Verify Installations:
Type the following in terminal to verify the installation of OpenCV:
```
python3
```
```
Python 3.12.3 (tags/v3.12.3:f6650f9, May  25 2025, 14:05:25) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> import numpy
>>>
```
The ```cv2``` and ```numpy``` modules should be imported into Python without any errors. This indicates that OpenCV module is correctly installed.


![image](https://github.com/user-attachments/assets/3005c205-4c0d-4624-b268-88d51c5519ad)

# Testing Electronic Components
1. HC-SR04 Ultrasonic Sensor: <br/>
     Connect the sensor pins to the Raspberry Pi as follows: <br/>
          TRIGGER - GPIO 18 (Pin 12) <br/>
          ECHO - GPIO 24 (Pin 18) <br/>
          VCC - 5V (Pin 2 or Pin 4) <br/>
          GND - GND (Pins 6, 9, 14, 25, 30 or 34) <br/>

   Run the python script ```ultra.py``` to check the sensor.
   ```
   python3 ultra.py
   ```

2. IR Sensor:
      Connect the sensor pins to the Raspberry Pi as follows: <br/>
         VCC - 5V <br/>
         GND - GND <br/>
         OUT - GPIO 17 (Pin 11) <br/>

  Run the python script ```ir.py``` to check the sensor.
   ```
   python3 ir.py
   ```

3. DC Motors with L298N:
     Connect the module to the Raspberry Pi as follows: <br/>
         IN1 - GPIO 5 (Pin 29) <br/>
         IN2 - GPIO 6 (Pin 31) <br/>
         IN3 - GPIO 19 (Pin 35) <br/>
         IN4 - GPIO 26 (Pin 37) <br/>
   
   Run the python script ```motor.py``` to check the motor driver and motors.
   ```
   python3 motor.py
   ```

4. Raspberry Pi Camera Module rev1.3:
      Connect the camera module to the CSI Port of the Raspberry Pi.
   ```
   ls /dev/video*
   ```
   This command should give a list of video interfaces available. Make sure that ```/dev/video0``` is listed.
   ```
   vcgencmd get_camera
   ```
   This command should show ```supported = 1 detected = 1```

   ```
   python3 picam.py
   ```
   Running this script should open the live camera feed from the Raspberry Pi Camera.

5. ```YOLOv4-tiny``` Model:
      Ensure that ```yolov4-tiny.cfg```, ```yolov4-tiny.weights``` and ```coco.names``` are in the same folder as all the scripts.
   ```
   python3 model.py
   ```
   This script enables person detection using the ```YOLOv4-tiny``` model on the live feed of the Raspberry Pi Camera.
   
   
