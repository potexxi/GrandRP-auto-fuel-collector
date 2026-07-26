import cv2
import numpy as np
import mss
import keyboard
import time
import pyautogui
from datetime import datetime

RESOLUTIONS = {
    "A": (2560, 1440),
    "B": (1920, 1080),
    "C": (3440, 1440),
    "D": (3840, 2160),
    "E": (1600, 900)
}

# MONITOR REGION AS PERCENTAGES
MONITOR_PERCENT = {
    "left": 0.84,
    "top": 0.72,
    "width": 0.005,
    "height": 0.031
}

# CLICK POSITION AS PERCENTAGES
CLICK_PERCENT = {
    "x": 0.08,   # 8% from left
    "y": 0.70    # 70% from top
}

def select_resolution():
    print("Please select your screen resolution:")
    for key, res in RESOLUTIONS.items():
        print(f"{key}) {res[0]}x{res[1]}")

    while True:
        choice = input("Your choice: ").upper().strip()
        if choice in RESOLUTIONS:
            width, height = RESOLUTIONS[choice]
            print(f"Selected resolution: {width}x{height}")
            return width, height
        else:
            print("Invalid option. Please try again.")

def calculate_monitor(screen_width, screen_height):
    left   = int(screen_width  * MONITOR_PERCENT["left"])
    top    = int(screen_height * MONITOR_PERCENT["top"])
    width  = int(screen_width  * MONITOR_PERCENT["width"])
    height = int(screen_height * MONITOR_PERCENT["height"])

    return {
        "left": left,
        "top": top,
        "width": width,
        "height": height
    }

def calculate_click_position(screen_width, screen_height):
    x = int(screen_width  * CLICK_PERCENT["x"])
    y = int(screen_height * CLICK_PERCENT["y"])
    return x, y

screen_w, screen_h = select_resolution()
MONITOR = calculate_monitor(screen_w, screen_h)
CLICK_X, CLICK_Y = calculate_click_position(screen_w, screen_h)

print("\nCalculated MONITOR region:")
print(MONITOR)
print("Calculated click position:", CLICK_X, CLICK_Y)
print("=" * 50)

LOWER_ORANGE = np.array([10, 120, 120])
UPPER_ORANGE = np.array([25, 255, 255])

LOWER_GREEN = np.array([45, 80, 80])
UPPER_GREEN = np.array([95, 255, 255])

print("F8  = Start")
print("F12 = Stop")
print("ESC = Exit program")
print("=" * 50)

running = False
last_press_time = 0
PRESS_INTERVAL = 0.25

with mss.MSS() as sct:
    while True:

        if keyboard.is_pressed("F8") and not running:
            running = True
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring started.")
            time.sleep(0.3)

        if keyboard.is_pressed("F12") and running:
            running = False
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring stopped.")
            time.sleep(0.3)

        if keyboard.is_pressed("esc"):
            print("Program terminated.")
            break

        if not running:
            time.sleep(0.05)
            continue

        img = np.array(sct.grab(MONITOR))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask_orange = cv2.inRange(hsv, LOWER_ORANGE, UPPER_ORANGE)
        mask_green  = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

        ys_orange = np.where(mask_orange > 0)[0]
        ys_green  = np.where(mask_green > 0)[0]

        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        orange_detected = len(ys_orange) > 0
        green_detected  = len(ys_green) > 0

        # ORANGE → press E repeatedly
        if orange_detected:
            if time.time() - last_press_time > PRESS_INTERVAL:
                print(f"[{now}] >>> Pressed E (orange detected) <<<")
                keyboard.press_and_release("e")
                last_press_time = time.time()
            continue

        # GREEN → do nothing
        if green_detected:
            print(f"[{now}] Green detected.")
            continue

        # NO BAR → left-click
        print(f"[{now}] No bar detected → Left-click executed.")
        pyautogui.click(x=CLICK_X, y=CLICK_Y)
        time.sleep(0.1)
