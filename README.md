# Tejas
Bot for Person Detection, Tracking, Obstacle Avoidance and Line Following for Resonance 1.0 Hardware Hackathon at KLE Technological University, Dr. M. S. Sheshgiri Campus, Belagavi

Electronic Components Required:
1. Raspberry Pi 4 Model B (8GB RAM recommended)
2. Micro SD Card (Class 10 32 GB recommended)
3. Micro SD Card Reader
4. HC-SR04 Ultrasonic Sensor
5. L298N Motor Driver
6. 60 RPM DC Geared Motors x 2
7. Raspberry Pi Camera rev1.3 or USB Webcam (USB Webcam is recommended)
8. IR Sensors x 3
9. 5V/3A Battery Elimination Circuit (BEC) for Raspberry Pi
10. Power Distribution Board
11. 12V to 5V step-down converter
12. 3-cell Lithium Battery (11.1V - 12.6V) (3S1P LiPo 3300mAh 35C battery recommended)
13. Micro Breadboard
14. Jumper wires - Male to Male, Male to Female, Female to Female (15 cm) (as required)
15. Single stranded wires (as required) 

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
NOTE: For optimal functionality:
   1. Use a micro-breadboard for common VCC (5V) and GND connection for all electronic components.
   2. Power the Raspberry Pi with 5V/3A Power supply seperately through a Battery Elimination Circuit (BEC).
   3. Power the common 5V and GND connections on the micro-breadboard seperately using another step-down converter.

This ensures that the power supply to the Raspberry Pi is not throttled down during operation.

Navigate to ```Test  ``` folder to find the scripts for testing electronic components

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

1. IR Sensors:<br/>
      Three IR Sensors are required for line following algorithm. One at the left (L), one at the centre (C) and one at the right (R). <br/> IR Sensor ouputs a ```0``` if ```black``` is detected and outputs a ```1``` if ```white``` is detected. <br/> <br/>
      
      | L | C | R | Action     |
      | - | - | - | ---------- |
      | 0 | 1 | 0 | Forward    |
      | 0 | 0 | 1 | Turn Right |
      | 1 | 0 | 0 | Turn Left  |
      | 1 | 1 | 0 | Hard Left  |
      | 0 | 1 | 1 | Hard Right |
      | 1 | 1 | 1 | Stop       |


      Connect the sensor pins to the Raspberry Pi as follows: <br/>
         VCC - 5V <br/>
         GND - GND <br/>
         LEFT IR: OUT - GPIO 17 (Pin 11) <br/>
         CENTRE IR: OUT - GPIO 27 (Pin 13) <br/>
         RIGHT IR: OUT - GPIO 22 (Pin 15) <br/>
   
  Run the python script ```ir.py``` to check the sensor.
   ```
   python3 ir.py
   ```

4. DC Motors with L298N:<br/>
     Connect the module to the Raspberry Pi as follows: <br/>
         IN1 - GPIO 5 (Pin 29) <br/>
         IN2 - GPIO 6 (Pin 31) <br/>
         IN3 - GPIO 19 (Pin 35) <br/>
         IN4 - GPIO 26 (Pin 37) <br/>
   
   Run the python script ```motor.py``` to check the motor driver and motors.
   ```
   python3 motor.py
   ```

5. Raspberry Pi Camera Module rev1.3:<br/>
   NOTE: If using a USB Webcam, connect it to the USB Port and skip this step and directly run ```cam.py``` script.<br/>
   Connect the camera module to the CSI Port of the Raspberry Pi.<br/>
   ```
   ls /dev/video*
   ```
   This command should give a list of video interfaces available. Make sure that ```/dev/video0``` is listed.
   ```
   vcgencmd get_camera
   ```
   This command should show ```supported = 1 detected = 1```

   ```
   python3 cam.py
   ```
   Running this script should open the live camera feed from the Camera. 

7. ```YOLOv4-tiny``` Model:
      Ensure that ```yolov4-tiny.cfg```, ```yolov4-tiny.weights``` and ```coco.names``` are in the same folder as all the scripts.
   ```
   python3 model.py
   ```
   This script enables person detection using the ```YOLOv4-tiny``` model on the live feed of the Raspberry Pi Camera.
