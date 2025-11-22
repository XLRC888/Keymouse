# Made by XLRC888
import keyboard
import mouse
import time
import atexit
import sys

BASE_SPEED = 10
SLOW_SPEED = 3
REFRESH_RATE = 0.01

print("="*40)
print("  by XLRC888 - Keymouse V1")
print("="*40)
print("Controls:")
print("  [Arrow Keys] : Move Mouse")
print("  [Left Shift] : Slow/Precision Mode")
print("  [Right Shift]: Left Click")
print("  [Menu Key]   : Right Click")
print("  [Page Up]    : Mouse Wheel Up")
print("  [Page Down]  : Mouse Wheel Down")
print("  [ESC]        : Quit Program")
print("=" * 40)
print("Status: RUNNING")
print("NOTE: You might need to run as Administrator/sudo for the keys to be detected by the code instead of the system.")

MOVE_KEYS = ['up', 'down', 'left', 'right']

CLICK_KEYS = {
    'right shift': 'left',
    'menu': 'right'
}

SCROLL_KEYS = {
    'page up': 1,
    'page down': -1
}

active_keys = {key: False for key in MOVE_KEYS}

def cleanup():
    """Unhooks all keyboard listeners to restore normal key function."""
    print("Attempting to restore normal key function...")
    keyboard.unhook_all()
    print("Cleanup complete. Keys restored.")

atexit.register(cleanup)


def start_move(event):
    """Callback when movement key is pressed. Updates state."""
    if event.name in active_keys:
        active_keys[event.name] = True

def stop_move(event):
    """Callback when movement key is released. Updates state."""
    if event.name in active_keys:
        active_keys[event.name] = False

def handle_click(key_name):
    """Handles mouse clicks based on the key pressed."""
    if keyboard.is_pressed(key_name):
        mouse.click(CLICK_KEYS[key_name])

def handle_scroll(key_name):
    """Handles mouse wheel scrolling based on the key pressed."""
    mouse.wheel(SCROLL_KEYS[key_name])

for key in MOVE_KEYS:
    keyboard.on_press_key(key, start_move, suppress=True) 
    keyboard.on_release_key(key, stop_move, suppress=True)

for key, mouse_button in CLICK_KEYS.items():
    keyboard.on_press_key(key, lambda e, k=key: handle_click(k), suppress=True)

for key, direction in SCROLL_KEYS.items():
    keyboard.on_press_key(key, lambda e, k=key: handle_scroll(k), suppress=True)

try:
    while True:
        if keyboard.is_pressed('esc'):
            print("\nESC pressed...")
            break

        dx = 0
        dy = 0
        
        current_speed = SLOW_SPEED if keyboard.is_pressed('shift') else BASE_SPEED

        if active_keys['up']:
            dy -= current_speed
        if active_keys['down']:
            dy += current_speed
        if active_keys['left']:
            dx -= current_speed
        if active_keys['right']:
            dx += current_speed

        if dx != 0 or dy != 0:
            mouse.move(dx, dy, absolute=False, duration=0)

        time.sleep(REFRESH_RATE)

except KeyboardInterrupt:
    print("\nProgram interrupted by user (Ctrl+C)...")
    pass