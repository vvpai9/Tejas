import RPi.GPIO as GPIO
import time

# Motor A pins
IN1 = 5
IN2 = 6

# Motor B pins
IN3 = 19
IN4 = 26

# IR sensor pin
IR_SENSOR = 21

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)
GPIO.setup(IR_SENSOR, GPIO.IN)

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
    motorB_forward()

def turnRight():
    motorA_forward()
    motorB_backward()    

def moveForward():
    motorA_forward()
    motorB_forward()

def is_obstacle_detected():
    return GPIO.input(IR_SENSOR) == 0

try:
    # print("Motors will run unless obstacle is detected via IR sensor.")

    moveForward()
    time.sleep(2)
    turnLeft()
    time.sleep(2)
    turnRight()
    time.sleep(2)
    stop_all()
    # while True:
    #     if is_obstacle_detected():
    #         print("Obstacle detected! Stopping motors.")
    #         stop_all()
    #     else:
    #         print("No obstacle. Motors running forward.")
    #         motorA_forward()
    #         motorB_forward()
    #     time.sleep(0.2)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    stop_all()
    GPIO.cleanup()
