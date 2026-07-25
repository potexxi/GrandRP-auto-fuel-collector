import cv2
import numpy as np
import mss
import keyboard
import time
import pyautogui
from datetime import datetime

MONITOR = {
    "left": 2155,
    "top": 1034,
    "width": 12,
    "height": 45
}

# Orange range
LOWER_ORANGE = np.array([10, 120, 120])
UPPER_ORANGE = np.array([25, 255, 255])

# Green range (bar visible but not orange)
LOWER_GREEN = np.array([45, 80, 80])
UPPER_GREEN = np.array([95, 255, 255])

print("F8  = Start")
print("F12 = Stop")
print("ESC = Exit program")
print("=" * 50)

running = False
last_press_time = 0
PRESS_INTERVAL = 0.25   # press E every 250ms while orange is visible

with mss.MSS() as sct:
    while True:

        # Start monitoring
        if keyboard.is_pressed("F8") and not running:
            running = True
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring started.")
            time.sleep(0.3)

        # Stop monitoring
        if keyboard.is_pressed("F12") and running:
            running = False
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring stopped.")
            time.sleep(0.3)

        # Exit program
        if keyboard.is_pressed("esc"):
            print("Program terminated.")
            break

        if not running:
            time.sleep(0.05)
            continue

        # Capture screen region
        img = np.array(sct.grab(MONITOR))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Masks
        mask_orange = cv2.inRange(hsv, LOWER_ORANGE, UPPER_ORANGE)
        mask_green  = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

        ys_orange = np.where(mask_orange > 0)[0]
        ys_green  = np.where(mask_green > 0)[0]

        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        orange_detected = len(ys_orange) > 0
        green_detected  = len(ys_green) > 0

        # 1) ORANGE → press E repeatedly
        if orange_detected:
            if time.time() - last_press_time > PRESS_INTERVAL:
                print(f"[{now}] >>> Pressed E (orange detected) <<<")
                keyboard.press_and_release("e")
                last_press_time = time.time()
            continue

        # 2) GREEN → do nothing
        if green_detected:
            print(f"[{now}] Green detected.")
            continue

        # 3) NO BAR → left-click
        print(f"[{now}] No bar detected → Left-click executed.")
        pyautogui.click(x=200, y=1300)  # adjust coordinates if needed
        time.sleep(0.1)
