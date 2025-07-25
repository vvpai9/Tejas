import RPi.GPIO as GPIO
import time

TRIG = 18
ECHO = 24
CALIBRATION_FACTOR = 1.0
MIN_VALID_DISTANCE = 2.0
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
print("Pins configured")

def get_distance(timeout=0.02):
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    print("Calculating distance...")
    pulse_start_time = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - pulse_start_time > timeout:
            print("Echo start timeout!")
            return None
    pulse_start = time.time()
        
        
    pulse_end_time = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - pulse_start_time > timeout:
            print("Echo end timeout!")
            return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 * CALIBRATION_FACTOR # Speed of sound / 2
    distance = round(distance, 2)
    #if distance < MIN_VALID_DISTANCE or distance > 400:
    #    return None
    return distance

try:
    while True:
        print("Trying to calculate distance")
        dist = get_distance()
        print(f"Distance to obstacle: {dist} cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user.")   
finally:
    GPIO.cleanup()
    print("GPIO cleanup done.")
