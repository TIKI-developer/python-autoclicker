import pyautogui
from pynput.keyboard import *
import time

#  ======== settings ========
delay = 2  # in seconds
duration = 10  # in seconds
resume_key = Key.f1
pause_key = Key.f2
exit_key = Key.esc
next_position_key = Key.right
clear_targets_key = Key.left
#  ==========================


targets = list()
isPaused = True
running = True
start_time = 0
isInfinite = True


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
        set_next_target()
    elif key == clear_targets_key:
        clear_targets()
    

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


def main():
    global isPaused, delay, duration, start_time

    isInfinite = False
    delay = float(input("Enter delay: "))
    duration = float(input("Enter duration or 0 to infinity clicks: "))

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