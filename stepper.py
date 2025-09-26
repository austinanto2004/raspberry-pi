import RPi.GPIO as GPIO
import time

# GPIO pins connected to ULN2003 IN1–IN4
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Define step sequence for 28BYJ-48 (full-step)
step_sequence = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

def set_step(step):
    GPIO.output(IN1, step[0])
    GPIO.output(IN2, step[1])
    GPIO.output(IN3, step[2])
    GPIO.output(IN4, step[3])

def stepper_rotate(steps, delay=0.002, reverse=False):
    for i in range(steps):
        if reverse:
            step = step_sequence[(7 - (i % 8))]
        else:
            step = step_sequence[i % 8]
        set_step(step)
        time.sleep(delay)

try:
    while True:
        print("Rotating forward...")
        stepper_rotate(512)   # ~1 revolution forward
        time.sleep(0.5)

        print("Rotating backward...")
        stepper_rotate(512, reverse=True)  # ~1 revolution backward
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    GPIO.cleanup()