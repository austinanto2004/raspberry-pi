import RPi.GPIO as GPIO
import time

# Pin setup
SERVO_PIN = 17   # GPIO17 (pin 11 on Raspberry Pi)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM on pin at 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    """Move servo to specified angle (0 to 180)."""
    duty = 2 + (angle / 18)   # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.005)         # very tiny delay (5 ms)

try:
    while True:
        # Sweep 0 to 180 super fast
        for angle in range(0, 181, 30):   # big step: 30°
            set_angle(angle)
            time.sleep(0.005)

        # Sweep 180 back to 0 super fast
        for angle in range(180, -1, -30):
            set_angle(angle)
            time.sleep(0.005)

except KeyboardInterrupt:
    print("\nExiting...")
    pwm.stop()
    GPIO.cleanup()