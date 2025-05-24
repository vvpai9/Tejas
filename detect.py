import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# GPIO setup
TRIG = 3
ECHO = 5
RIGHT1 = 16  # Motor control pins
RIGHT2 = 18
LEFT1 = 11
LEFT2 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(RIGHT1, GPIO.OUT)
GPIO.setup(RIGHT2, GPIO.OUT)
GPIO.setup(LEFT1, GPIO.OUT)
GPIO.setup(LEFT2, GPIO.OUT)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound / 2
    return round(distance, 2)

def stop_bot():
    GPIO.output(RIGHT1, GPIO.LOW)
    GPIO.output(RIGHT2, GPIO.LOW)
    GPIO.output(LEFT1, GPIO.LOW)
    GPIO.output(LEFT2, GPIO.LOW)

def move_forward():
    GPIO.output(RIGHT1, GPIO.HIGH)
    GPIO.output(RIGHT2, GPIO.HIGH)
    GPIO.output(LEFT1, GPIO.HIGH)
    GPIO.output(LEFT2, GPIO.HIGH)

def move_left():
    GPIO.output(RIGHT1, GPIO.HIGH)
    GPIO.output(RIGHT2, GPIO.LOW)
    GPIO.output(LEFT1, GPIO.LOW)
    GPIO.output(LEFT2, GPIO.HIGH)

def move_right():
    GPIO.output(RIGHT1, GPIO.HIGH)
    GPIO.output(RIGHT2, GPIO.LOW)
    GPIO.output(LEFT1, GPIO.HIGH)
    GPIO.output(LEFT2, GPIO.LOW)

stop_bot()  # Ensure motors are stopped initially

# Load YOLOv4 Tiny
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

# Load COCO classes
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getUnconnectedOutLayersNames()
cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

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
            stop_bot()
            print("Obstacle too close! Stopping.")
        elif person_detected:
            if 0 <= center_x <= 213:
                move_left()
                print("Person detected. Moving left.")
            elif 213 < center_x <= 426:
                move_forward()
                print("Person detected. Moving forward.")
            elif 426 < center_x <= 640:
                move_right()
                print("Person detected. Moving right.")
        else:
            stop_bot()
            print("No person. Waiting.")

        cv2.imshow("Bot View", frame)
        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    cap.release()
    GPIO.cleanup()
    cv2.destroyAllWindows()
