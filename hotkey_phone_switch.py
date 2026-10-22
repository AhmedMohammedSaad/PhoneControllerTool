"""
Ultra-Focused Phone Switcher & Clean Mouse/Keyboard Controller
- Click Left: Open / Click / Touch anything naturally.
- Click Right: Back (رجوع خطوة للخلف).
- Mouse Wheel: Fast Smooth Scroll.
- Arrow Up / Down: Natural smooth scrolling.
- Alt + Space: Toggle IN and OUT cleanly.
- Escape: Exit Phone back to PC immediately.
"""

import os
import sys
import time
import subprocess
import threading
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    user32.SetProcessDPIAware()

CREATE_NO_WINDOW = 0x08000000
STARTUPINFO = subprocess.STARTUPINFO()
STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
STARTUPINFO.wShowWindow = 0

scrcpy_proc = None
hwnd_receiver = 0
is_on_phone = False
cached_serial = None
lock = threading.Lock()

def get_scrcpy_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(current_dir, "scrcpy.exe")
    if os.path.exists(p):
        return p
    return "scrcpy"

def get_physical_device_serial():
    global cached_serial
    if cached_serial:
        return cached_serial
    try:
        out = subprocess.check_output(
            ["adb", "devices"],
            encoding="utf-8",
            creationflags=CREATE_NO_WINDOW,
            startupinfo=STARTUPINFO
        )
        lines = out.strip().splitlines()
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 2 and parts[1] == "device":
                serial = parts[0]
                if not serial.startswith("emulator-"):
                    cached_serial = serial
                    return serial
    except Exception:
        pass
    return None

def adb_cmd(args):
    serial = get_physical_device_serial()
    cmd = ["adb"]
    if serial:
        cmd.extend(["-s", serial])
    cmd.extend(args)
    subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
        startupinfo=STARTUPINFO
    )

def scroll_down():
    adb_cmd(["shell", "input", "swipe", "360", "1050", "360", "650", "70"])

def scroll_up():
    adb_cmd(["shell", "input", "swipe", "360", "650", "360", "1050", "70"])

def start_scrcpy():
    global scrcpy_proc, hwnd_receiver
    scrcpy_bin = get_scrcpy_path()
    serial = get_physical_device_serial()

    # Right click = BACK (b), Left click = Touch (+), Middle = HOME (h)
    cmd = [
        scrcpy_bin,
        "--no-video",
        "--no-audio",
        "--keyboard=uhid",
        "--mouse=uhid",
        "--mouse-bind=bhsn:++++",
        "--window-title=NativePhoneMaster",
        "--window-x=10",
        "--window-y=10",
        "--window-width=48",
        "--window-height=48",
        "--window-borderless",
        "--always-on-top"
    ]

    if serial:
        cmd.extend(["-s", serial])
    else:
        cmd.append("-d")

    scrcpy_proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
        startupinfo=STARTUPINFO
    )

    for _ in range(30):
        time.sleep(0.15)
        hwnd_receiver = user32.FindWindowW(None, "NativePhoneMaster")
        if hwnd_receiver:
            break

    time.sleep(0.5)
    release_grab()

def release_grab():
    """Breaks scrcpy grab returning mouse/keyboard to Windows PC."""
    VK_LMENU = 0xA4
    user32.keybd_event(VK_LMENU, 0x38, 0, 0)
    time.sleep(0.01)
    user32.keybd_event(VK_LMENU, 0x38, 2, 0)

def switch_to_phone():
    global is_on_phone, hwnd_receiver
    if hwnd_receiver:
        user32.SetWindowPos(hwnd_receiver, -1, 10, 10, 48, 48, 0x0040)
        user32.ShowWindow(hwnd_receiver, 5)
        user32.SetForegroundWindow(hwnd_receiver)
        
        # Click naturally once to activate UHID focus
        user32.SetCursorPos(24, 24)
        user32.mouse_event(0x0002, 0, 0, 0, 0) # MOUSEEVENTF_LEFTDOWN
        time.sleep(0.01)
        user32.mouse_event(0x0004, 0, 0, 0, 0) # MOUSEEVENTF_LEFTUP

        with lock:
            is_on_phone = True

def switch_to_pc():
    global is_on_phone
    release_grab()
    # Move mouse back to center of PC screen
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)
    user32.SetCursorPos(w // 2, h // 2)
    with lock:
        is_on_phone = False

def is_down(vk):
    return (user32.GetAsyncKeyState(vk) & 0x8000) != 0

def monitor_loop():
    global is_on_phone
    VK_SPACE = 0x20
    VK_MENU = 0x12       # Alt
    VK_ESCAPE = 0x1B     # Esc
    VK_UP = 0x26         # Up Arrow
    VK_DOWN = 0x28       # Down Arrow
    VK_CONTROL = 0x11

    last_toggle = False
    last_esc = False
    last_scroll_time = 0

    while True:
        time.sleep(0.015)

        alt = is_down(VK_MENU)
        space = is_down(VK_SPACE)
        esc = is_down(VK_ESCAPE)
        ctrl = is_down(VK_CONTROL)

        # 1. Alt + Space: Toggle IN and OUT
        toggle = alt and space
        if toggle and not last_toggle:
            if is_on_phone:
                switch_to_pc()
            else:
                switch_to_phone()
            time.sleep(0.35)
            last_toggle = toggle
            continue
        last_toggle = toggle

        # 2. Esc: Exit Phone to PC immediately
        if is_on_phone and esc and not last_esc:
            switch_to_pc()
            time.sleep(0.3)
            last_esc = esc
            continue
        last_esc = esc

        # 3. السكرول بالأسهم
        if is_on_phone and not alt and not ctrl:
            now = time.time()
            if now - last_scroll_time >= 0.14:
                if is_down(VK_DOWN):
                    scroll_down()
                    last_scroll_time = now
                    continue
                elif is_down(VK_UP):
                    scroll_up()
                    last_scroll_time = now
                    continue

def main():
    t_scrcpy = threading.Thread(target=start_scrcpy, daemon=True)
    t_scrcpy.start()

    time.sleep(1.2)
    monitor_loop()

if __name__ == "__main__":
    main()
