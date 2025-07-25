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

def moveForward():
    motorA_backward()
    motorB_forward()
    
def moveBackward():
    motorA_forward()
    motorB_backward()

def turnRight():
    motorA_forward()
    motorB_forward()

stop_all()  # Ensure motors are stopped initially


try:
    print("Moving forward")
    moveForward()
    time.sleep(2)
    print("Left")
    turnLeft()
    time.sleep(2)
    print("Right")
    turnRight()
    time.sleep(2)
    print("Backward")
    moveBackward()
    time.sleep(2)
    stop_all()
    
except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    stop_all()
    GPIO.cleanup()
