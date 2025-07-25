import RPi.GPIO as GPIO
import time

# GPIO pin setup
IR_LEFT = 17
IR_CENTER = 27
IR_RIGHT = 22

def setup():
    GPIO.setmode(GPIO.BCM)
    
    # IR Sensors
    GPIO.setup(IR_LEFT, GPIO.IN)
    GPIO.setup(IR_CENTER, GPIO.IN)
    GPIO.setup(IR_RIGHT, GPIO.IN)
    
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

def loop():
    while True:
        l = GPIO.input(IR_LEFT)
        c = GPIO.input(IR_CENTER)
        r = GPIO.input(IR_RIGHT)

        if l == 0 and c == 1 and r == 0:
            forward()
        elif l == 0 and c == 0 and r == 1:
            right()
        elif l == 1 and c == 0 and r == 0:
            left()
        elif l == 1 and c == 1 and r == 0:
            left()
        elif l == 0 and c == 1 and r == 1:
            right()
        elif l == 1 and c == 1 and r == 1:
            stop()
        else:
            stop()  # fallback
        time.sleep(0.05)

def destroy():
    stop()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
