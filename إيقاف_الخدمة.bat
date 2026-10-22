@echo off
chcp 65001 >nul
taskkill /F /IM scrcpy.exe >nul 2>&1
wmic process where "commandline like '%%hotkey_phone_switch.py%%'" delete >nul 2>&1
wmic process where "commandline like '%%mini_phone_widget.py%%'" delete >nul 2>&1
echo تم إيقاف جميع خدمات التحكم بنجاح.
timeout /t 2 >nul
