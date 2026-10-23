# PhoneControllerTool 📱⚡

> **Seamless, ultra-responsive PC-to-Android hardware control tool.** Control your physical Android phone using your PC's mouse and keyboard with zero latency, instant hotkey switching (`Alt + Space`), and zero video streaming lag.

---

## 🌟 Overview

**PhoneControllerTool** bridges the gap between Windows PC and physical Android devices. Unlike traditional screen mirroring tools that stream heavy video frames and introduce mouse lag, this tool leverages **scrcpy UHID (USB HID)** emulation. Your mouse and keyboard act as direct physical USB/Bluetooth peripherals plugged into your phone, giving you 100% native responsiveness.

With a single hotkey (`Alt + Space`), you can toggle your cursor and keystrokes instantly between your Windows PC desktop and your phone!

---

## 🚀 Key Features

* **Instant Hotkey Switching (`Alt + Space`)**: Switch back and forth between PC and Phone in milliseconds.
* **Instant Escape (`Esc`)**: Instantly breaks focus and returns your mouse cursor to the center of your PC screen.
* **Hardware Mouse Control**:
  * **Left Click**: Open apps, tap, touch, drag naturally.
  * **Right Click**: Android **Back** button.
  * **Middle Click / Scroll Wheel Click**: Android **Home** button.
  * **Mouse Wheel**: Fast native scroll.
* **Smooth Arrow Scrolling**: Arrow Up & Arrow Down provide human-like, smooth scrolling inside chats, social media feeds, and long documents.
* **Windows-like Keystrokes & Media**:
  * Volume control (`Alt + Up` / `Alt + Down`).
  * Brightness control (`Alt + Right` / `Alt + Left`).
  * Home Screen (`Home` or `Win + D`).
  * Recent Apps (`Alt + Tab`).
  * Screen Lock (`Win + L`).
* **Floating Widget Mode**: Optional discrete 48x48 floating top-left widget that stays hidden from the Taskbar and Alt+Tab.
* **100% Silent Background Execution**: Runs via invisible VBScript launchers without annoying command prompt windows.

---

## ⌨️ Shortcut Cheat Sheet

| Shortcut | Action | Description |
| :--- | :--- | :--- |
| **`Alt + Space`** | **Toggle PC ⟷ Phone** | Jump your mouse & keyboard into the phone or back to PC |
| **`Escape`** | **Exit to PC** | Instantly return mouse cursor to your PC screen |
| **`Left Click`** | **Tap / Click** | Standard touch & tap on phone screen |
| **`Right Click`** | **Back** | Android back button |
| **`Middle Click`** | **Home** | Return to Phone Home screen |
| **`Arrow Down`** | **Scroll Down** | Smooth natural scrolling down |
| **`Arrow Up`** | **Scroll Up** | Smooth natural scrolling up |
| **`Alt + Up`** | **Volume Up** | Increase phone volume |
| **`Alt + Down`** | **Volume Down** | Decrease phone volume |
| **`Alt + Right`** | **Brightness Up** | Increase phone screen brightness |
| **`Alt + Left`** | **Brightness Down** | Decrease phone screen brightness |
| **`Alt + Tab`** | **Recent Apps** | Open Android multitasking app switcher |
| **`Win + D` / `Home`**| **Home Screen** | Minimize everything to Home screen |
| **`Win + L`** | **Lock Screen** | Lock phone display |

---

## 📋 Prerequisites

1. **Windows 10 or Windows 11**.
2. **Python 3.8+** installed and added to system PATH.
3. **Android Device** with **USB Debugging** enabled:
   * Go to `Settings` → `About phone` → Tap `Build number` 7 times.
   * Go to `Settings` → `Developer options` → Turn on **USB Debugging**.
   * (On Xiaomi / Realme / Oppo): Also enable **USB debugging (Security settings)** to allow touch/keyboard inputs.

---

## 🛠️ Quick Start Guide

1. Clone or download this repository:
   ```bash
   git clone https://github.com/AhmedMohammedSaad/PhoneControllerTool.git
   cd PhoneControllerTool
   ```
2. Connect your Android phone to your PC via a USB cable. Accept the "Allow USB Debugging" prompt on your phone screen.
3. Launch the controller:
   * Double-click **`تشغيل_باختصار_الكيبورد.vbs`** (Silent mode with hotkeys).
   * Or run via Python:
     ```bash
     python hotkey_phone_switch.py
     ```
4. Press **`Alt + Space`** to start controlling your phone!
5. To stop the service: Double-click **`إيقاف_الخدمة.bat`**.

---

## 📂 Project Structure

```
PhoneControllerTool/
├── hotkey_phone_switch.py            # Main switcher script with hotkey listeners & UHID integration
├── mini_phone_widget.py              # Floating UI widget alternative
├── تشغيل_باختصار_الكيبورد.vbs        # Silent background launcher for hotkey switcher
├── أيقونة_الموبايل_العائمة.vbs       # Silent background launcher for floating widget
├── إيقاف_الخدمة.bat                  # One-click service terminator
├── دليل_اختصارات_الكيبورد.txt        # Arabic keyboard quick reference
├── دليل_اختصارات_الويندوز_للموبايل.txt # Windows shortcuts reference
├── scrcpy.exe & adb.exe              # Embedded lightweight ADB & scrcpy runtime binaries
└── README.md                         # Documentation
```

---

## 🇪🇬 ملخص سريع بالعربية (Arabic Summary)

**أداة التحكم السريع في الهاتف من الكمبيوتر (PhoneControllerTool):**
* تحكم كامل في الموبايل بالماوس والكيبورد بدون أي لاج (باستخدام محاكاة الهاردوير UHID).
* التبديل الفوري بين شاشة اللابتوب والموبايل بضغطة زر واحدة: **`Alt + Space`**.
* الخروج الفوري للكمبيوتر بزر **`Esc`**.
* كليك يمين للرجوع للخلف، وسكرول ناعم بالأسهم وبكرة الماوس.
* تحكم في الصوت والإضاءة والتطبيقات المفتوحة واختصارات الويندوز المعتادة.


