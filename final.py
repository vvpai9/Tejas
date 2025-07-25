import cv2
import numpy as np
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import RPi.GPIO as GPIO

# Motor A pins
IN1 = 5
IN2 = 6

# Motor B pins
IN3 = 19
IN4 = 26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)

def motorA_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def motorB_forward():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def motorA_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def motorB_backward():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop_all():
    GPIO.output([IN1, IN2, IN3, IN4], GPIO.LOW)

def turnLeft():
    motorA_backward()
    motorB_backward()

def turnRight():
    motorA_forward()
    motorB_forward()

def moveForward():
    motorA_backward()
    motorB_forward()

stop_all()  # Ensure motors are stopped initially
factory = PiGPIOFactory()
sensor = DistanceSensor(trigger=18, echo=24, pin_factory=factory)  # Distance sensor pins

def get_distance():
    # Convert to centimeters and round
    distance_cm = round(sensor.distance * 100, 2)
    return distance_cm

net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# Load COCO classes
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getUnconnectedOutLayersNames()
cap = cv2.VideoCapture(0)

try:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        count += 1
        if count % 10 != 0:  # Process every 10th frame
            continue
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(layer_names)
        h, w = frame.shape[:2]
        center_x = 320

        person_detected = False
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                if classes[class_id] == "person" and scores[class_id] > 0.5:
                    box = detection[0:4] * np.array([w, h, w, h])
                    x, y, bw, bh = box.astype("int")
                    center_x = x
                    person_detected = True
                    cv2.rectangle(frame, (x - bw//2, y - bh//2), (x + bw//2, y + bh//2), (0, 255, 0), 2)
                    break
        
        dist = get_distance()
        print(f"Distance to obstacle: {dist} cm | Person Detected: {person_detected}")

        if dist < 10:
            stop_all()
            print("Obstacle too close! Stopping.")
        elif person_detected:
            if 0 <= center_x <= 213:
                turnLeft()
                print("Person detected. Moving left.")
            elif 213 < center_x <= 426:
                moveForward()
                print("Person detected. Moving forward.")
            elif 426 < center_x <= 640:
                turnRight()
                print("Person detected. Moving right.")
        else:
            stop_all()
            print("No person. Waiting.")
        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    stop_all()
    GPIO.cleanup()
