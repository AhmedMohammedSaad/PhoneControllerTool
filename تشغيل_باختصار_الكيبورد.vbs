Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' تشغيل السكربت في صمت تام بدون أي تيرمينال
WshShell.Run "pythonw """ & currentDir & "\hotkey_phone_switch.py""", 0, False
