import subprocess
import pyautogui

def execute_intent(intent):
    """Execute only predefined and whitelisted intents."""
    if intent == "OPEN_CALCULATOR":
        try:
            subprocess.Popen(["calc.exe"])
            return True, "Calculator opened successfully."
        except Exception as e:
            return False, f"Could not open Calculator: {e}"
    elif intent == "OPEN_BROWSER":
        try:
            subprocess.Popen(
                ["cmd", "/c", "start", "", "https://www.google.com"],
                shell=False
            )
            return True, "Browser opened successfully."
        except Exception as e:
            return False, f"Could not open Browser: {e}"
    elif intent == "OPEN_TEXT_EDITOR":
        try:
            subprocess.Popen(["notepad.exe"])
            return True, "Text editor opened successfully."
        except Exception as e:
            return False, f"Could not open Text Editor: {e}"
    elif intent == "SCROLL_UP":
        pyautogui.scroll(5)
        return True, "Scrolled up."
    elif intent == "SCROLL_DOWN":
        pyautogui.scroll(-5)
        return True, "Scrolled down."
    elif intent == "CLOSE_APPLICATION":
        try:
            pyautogui.hotkey("alt", "f4")
            return True, "Active application closed."
        except Exception as e:
            return False, f"Could not close application: {e}"
    elif intent == "OPEN_FILE_EXPLORER":
        try:
            subprocess.Popen(["explorer.exe"])
            return True, "File Explorer opened successfully."
        except Exception as e:
            return False, f"Could not open File Explorer: {e}"
    elif intent == "TAKE_SCREENSHOT":
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            return True, "Screenshot saved as screenshot.png."
        except Exception as e:
            return False, f"Could not take screenshot: {e}"
    elif intent == "VOLUME_UP":
        try:
            pyautogui.press("volumeup")
            return True, "Volume increased."
        except Exception as e:
            return False, f"Could not increase volume: {e}"
    elif intent == "VOLUME_DOWN":
        try:
            pyautogui.press("volumedown")
            return True, "Volume decreased."
        except Exception as e:
            return False, f"Could not decrease volume: {e}"
    else:
        return False, "Unknown or unsupported intent. No action taken."