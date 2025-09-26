import RPi.GPIO as GPIO
import time
import tkinter as tk

# Servo setup
SERVO_PIN = 17   # GPIO17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# 50Hz PWM
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    """Move servo to specific angle (0–180)."""
    duty = 2 + (int(angle) / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)
    pwm.ChangeDutyCycle(0)   # stop signal to reduce jitter

# --- Tkinter GUI ---
root = tk.Tk()
root.title("Servo Motor Control")
root.geometry("300x250")

# Slider control
angle_var = tk.DoubleVar()

def update_angle(val):
    set_angle(float(val))

slider = tk.Scale(root, from_=0, to=180,
                  orient="horizontal", length=250,
                  variable=angle_var, command=update_angle,
                  label="Servo Angle")
slider.pack(pady=20)

# Quick buttons
frame = tk.Frame(root)
frame.pack(pady=10)

btn0 = tk.Button(frame, text="0°", width=8, command=lambda: set_angle(0))
btn0.grid(row=0, column=0, padx=5)

btn90 = tk.Button(frame, text="90°", width=8, command=lambda: set_angle(90))
btn90.grid(row=0, column=1, padx=5)

btn180 = tk.Button(frame, text="180°", width=8, command=lambda: set_angle(180))
btn180.grid(row=0, column=2, padx=5)

# Exit cleanup
def on_close():
    pwm.stop()
    GPIO.cleanup()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()