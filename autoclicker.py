import pyautogui
from pynput.keyboard import *
import time
import math

#  ======== settings ========
delay = 2  # in seconds
duration = 10  # in seconds
resume_key = Key.f1
pause_key = Key.f2
exit_key = Key.esc
next_position_key = Key.right
clear_targets_key = Key.left
setup_key = Key.down
change_target_set_mode_key = Key.up
#  ==========================


targets = list()
isPaused = True
running = True
start_time = 0
isInfinite = True
isSmartModeClickFirst = True
p1 = (0, 0)
p2 = (0, 0)
mode = "d" #d - default, s - smart

def divide_line_segment(p1, p2, interval):
    x1, y1 = p1
    x2, y2 = p2
    points = [p1]

    # Calculate the distance between the two points
    distance = math.hypot(x2 - x1, y2 - y1)

    # Calculate the number of intervals
    num_intervals = int(distance / interval)

    # Calculate the increment in x and y directions
    dx = (x2 - x1) / num_intervals
    dy = (y2 - y1) / num_intervals

    # Generate points
    for i in range(1, num_intervals):
        x = x1 + i * dx
        y = y1 + i * dy
        points.append((x, y))

    points.append(p2)  # Add the end point
    return points


def clear_targets():
    targets.clear()

def pause():
    global isPaused, start_time
    isPaused = True
    start_time = time.time()
    print("[Paused]")

def resume():
    global isPaused, start_time
    isPaused = False
    start_time = time.time()
    print("[Resumed]")


def on_press(key):
    global running, isPaused

    if key == resume_key:
        resume()
    elif key == pause_key:
        pause()
    elif key == exit_key:
        running = False
        print("[Exit]")
    elif key == next_position_key:
        if mode == "d":
            set_next_target()
        elif mode == "s":
            set_next_target_with_smart_mode()
    elif key == clear_targets_key:
        clear_targets()
    elif key == setup_key:
        if (isPaused):
            setup()
    elif key == change_target_set_mode_key:
        change_mode()
    

def change_mode():
    global mode

    if mode == "s":
        mode = "d"
        print("Mode set to default")
    elif mode == "d":
        mode = "s"
        print("Mode set to smart")

def set_next_target_with_smart_mode():
    global isSmartModeClickFirst, p1, p2

    if isSmartModeClickFirst:
        p1 = pyautogui.position()
        isSmartModeClickFirst = False
        return
    else:
        p2 = pyautogui.position()
        interval = float(input("Enter interval: "))
        points = divide_line_segment(p1, p2, interval)
        targets.extend(points)
        isSmartModeClickFirst = True

def set_next_target():
    pos = pyautogui.position()
    print("Added target with position: " + str(pos))
    targets.append(pos)
    return


def display_controls():
    print("// AutoClicker by iSayChris")
    print("// - Settings: ")
    print("\t delay = " + str(delay) + 'ec' + '\n')
    print("\t duration = " + str(duration) + 'ec' + '\n')
    print("// - Controls:")
    print("\t F1 = Resume")
    print("\t F2 = Pause")
    print("\t F3 = Exit")
    print("-----------------------------------------------------")
    print('Press F1 to start...')

def setup():
    global delay, duration
    delay = float(input("Enter delay: "))
    duration = float(input("Enter duration or 0 to infinity clicks: "))

def main():
    global isPaused, delay, duration, start_time

    isInfinite = False
    setup()

    if (duration == 0):
        isInfinite = True

    lis = Listener(on_press=on_press)

    lis.start()

    display_controls()
    start_time = time.time()
    while running:
        if not isPaused:
            for target in targets:
                pyautogui.click(target)
                pyautogui.PAUSE = delay
            if time.time() - start_time >= duration and not isInfinite:
                pause()
    lis.stop()


if __name__ == "__main__":
    main()