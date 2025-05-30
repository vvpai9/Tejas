from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import time

factory = PiGPIOFactory()
sensor = DistanceSensor(trigger=18, echo=24, pin_factory=factory)

while True:
    time.sleep(2)
    
    # Convert to centimeters and round
    distance_cm = round(sensor.distance * 100, 2)
    
    print("Distance: {} cm".format(distance_cm))
