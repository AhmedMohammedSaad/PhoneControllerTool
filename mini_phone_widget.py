"""
Mini Floating Phone Widget
- Sizes the scrcpy OTG window into a small floating icon (50x50).
- Positions it at top-left.
- Hides it COMPLETELY from Windows Taskbar and Alt+Tab (WS_EX_TOOLWINDOW).
- Always on Top.
- Clicking it immediately enters physical phone mouse.
- Pressing (Left Alt) returns mouse to PC.
"""

import os
import sys
import time
import subprocess
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    user32.SetProcessDPIAware()

GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOPMOST = 0x00000008
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020

def get_scrcpy_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(current_dir, "scrcpy.exe")
    if os.path.exists(p):
        return p
    return "scrcpy"

def main():
    CREATE_NO_WINDOW = 0x08000000
    scrcpy_bin = get_scrcpy_path()

    # أبعاد وموقع الأيقونة العائمة الصغيرة: أعلى الشمال (Top-Left)
    widget_x = 20
    widget_y = 60
    widget_w = 48
    widget_h = 48

    cmd = [
        scrcpy_bin,
        "-d",
        "--otg",
        "-M",
        "--window-title=PhoneMiniWidget",
        f"--window-x={widget_x}",
        f"--window-y={widget_y}",
        f"--window-width={widget_w}",
        f"--window-height={widget_h}",
        "--always-on-top",
        "--window-borderless"
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW
    )

    hwnd = 0
    for _ in range(30):
        time.sleep(0.15)
        hwnd = user32.FindWindowW(None, "PhoneMiniWidget")
        if hwnd:
            break

    if hwnd:
        # 1. إخفاء النافذة نهائياً من شريط المهام (Taskbar)
        ex_style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        ex_style = (ex_style | WS_EX_TOOLWINDOW | WS_EX_TOPMOST) & ~WS_EX_APPWINDOW
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)

        # 2. تثبيت الحجم والموقع والمقدمة وتحديث الإطار
        user32.SetWindowPos(
            hwnd,
            HWND_TOPMOST,
            widget_x,
            widget_y,
            widget_w,
            widget_h,
            SWP_FRAMECHANGED
        )

        # 3. تحرير الماوس فوراً عند البدء ليبقى الماوس حراً على شاشة اللاب
        user32.keybd_event(0xA4, 0x38, 0, 0)
        user32.keybd_event(0xA4, 0x38, 2, 0)

    try:
        while proc.poll() is None:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        if proc.poll() is None:
            proc.terminate()

if __name__ == "__main__":
    main()
