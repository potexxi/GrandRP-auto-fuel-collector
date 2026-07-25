# GrandRP-auto-fuel-collector
Collects automatic benzin (will be expanded to all three oil-types) on grand rp at the new oil plattformers.<br>
Generates ~200 pieces in 1 hour.
This script does not automatically pass the humen authentification. You need to do it manually.<br>
How to use it? -> [#supported-resolutions]

#### Use at your own risk. 

## Overview

This Python script monitors a small region of the screen and reacts based on the detected color state:

- **Orange detected** → Presses the **E** key repeatedly.
- **Green detected** → Does nothing.
- **No color bar detected** → Performs a left mouse click at predefined coordinates, to restart the produktion.

The monitored region is dynamically calculated based on the selected screen resolution.

## Features

- Supports multiple screen resolutions
- Start/stop monitoring using hotkeys
- Detects orange and green UI elements using HSV color ranges
- Automatically presses the **E** key while orange is visible
- Automatically executes a left mouse click when no bar is detected
- Lightweight screen capture using MSS

## Requirements

### Python Version

- Python 3.8 or newer

### Required Packages

Install all dependencies with:

```bash
pip install opencv-python numpy mss keyboard pyautogui
```

### Imports Used

```python
import cv2
import numpy as np
import mss
import keyboard
import time
import pyautogui
from datetime import datetime
```

## Supported Resolutions

When starting the script, select one of the following resolutions:

| Option | Resolution |
|----------|------------|
| A | 2560 × 1440 |
| B | 1920 × 1080 |
| C | 3440 × 1440 |
| D | 3840 × 2160 |
| E | 1600 × 900 |

The script calculates the monitoring area automatically based on the selected resolution. 
#### Please be sure, to have the default scale: 16:9. Otherwise it will not work correct.

## Controls

| Key | Function |
|-------|----------|
| F8 | Start monitoring |
| F12 | Stop monitoring |
| ESC | Exit the program |

## Usage

### 1. Start the Script

```bash
python main.py
```

### 2. Select Your Resolution

Example:

```text
Please select your screen resolution:
A) 2560x1440
B) 1920x1080
C) 3440x1440
D) 3840x2160
E) 1600x900

Your choice: B
```

### 3. Start Monitoring

Press:

```text
F8
```

Console output:

```text
[12:30:15] Monitoring started.
```

### 4. Stop Monitoring

Press:

```text
F12
```

Console output:

```text
[12:35:02] Monitoring stopped.
```

### 5. Exit

Press:

```text
ESC
```

## Configuration

### Monitor Region

The monitored area is defined as percentages of the selected screen resolution:

```python
MONITOR_PERCENT = {
    "left": 0.84,
    "top": 0.72,
    "width": 0.005,
    "height": 0.031
}
```

You can adjust these values if the target UI element appears at a different screen location.

### Click Position

Modify the click coordinates if necessary:

```python
pyautogui.click(x=200, y=1300)
```

---

## Example Output

```text
Calculated MONITOR region:
{'left': 1612, 'top': 777, 'width': 9, 'height': 33}
==================================================
F8  = Start
F12 = Stop
ESC = Exit program
==================================================

[15:12:04] Monitoring started.
[15:12:08.211] >>> Pressed E (orange detected) <<<
[15:12:08.461] >>> Pressed E (orange detected) <<<
[15:12:10.512] Green detected.
[15:12:11.031] No bar detected → Left-click executed.
```

## Notes

- The script must have permission to capture the screen and send keyboard/mouse input.
- The selected monitor region should be adjusted if the UI layout differs from your setup.
- Color ranges may require fine tuning depending on display settings, game graphics, or color filters.
- Running the script with administrator privileges may be required on some systems for global keyboard detection.

## License

This project is provided as-is for educational and personal use.