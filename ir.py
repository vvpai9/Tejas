from gpiozero import DigitalInputDevice
from signal import pause

# Connect the OUT pin of the IR sensor to GPIO21
ir_sensor = DigitalInputDevice(21)

def object_detected():
    print("🔴 Object Detected!")

def object_not_detected():
    print("✅ Path is Clear")

# When sensor output goes high (object not detected)
ir_sensor.when_activated = object_not_detected

# When sensor output goes low (object detected)
ir_sensor.when_deactivated = object_detected

print("🚦 IR Sensor is running... Press Ctrl+C to exit.")
pause()  # Keeps the script running