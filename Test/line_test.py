import RPi.GPIO as GPIO
import time

# GPIO pin setup
IR_LEFT = 17
IR_CENTER = 27
IR_RIGHT = 22

IN1 = 23  # Left motor
IN2 = 24
IN3 = 5   # Right motor
IN4 = 6

def setup():
    GPIO.setmode(GPIO.BCM)
    
    # IR Sensors
    GPIO.setup(IR_LEFT, GPIO.IN)
    GPIO.setup(IR_CENTER, GPIO.IN)
    GPIO.setup(IR_RIGHT, GPIO.IN)
    
    # Motor pins
    motor_pins = [IN1, IN2, IN3, IN4]
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def forward():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def stop():
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, False)

def left():
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)

def right():
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)

def loop():
    while True:
        l = GPIO.input(IR_LEFT)
        c = GPIO.input(IR_CENTER)
        r = GPIO.input(IR_RIGHT)

        if l == 0 and c == 1 and r == 0:
            print("Moving Forward")
        elif l == 0 and c == 0 and r == 1:
            print("Turning Right")
        elif l == 1 and c == 0 and r == 0:
            print("Turning Left")
        elif l == 1 and c == 1 and r == 0:
            print("Turning Left ")
        elif l == 0 and c == 1 and r == 1:
            print("Turning Right")
        elif l == 1 and c == 1 and r == 1:
            print("stop")
        else:
            print("Stop")  # fallback
        time.sleep(0.05)

def destroy():
    # stop()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        # setup()
        loop()
    except KeyboardInterrupt:
        destroy()
