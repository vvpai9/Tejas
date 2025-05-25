from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(trigger=18, echo=24)

while True:
    sleep(2)
    
    # Convert to centimeters and round
    distance_cm = round(sensor.distance * 100, 2)
    
    print("Distance: {} cm".format(distance_cm))
