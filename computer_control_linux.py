import subprocess

def execute_intent(intent):
    """Execute only predefined and whitelisted intents (Linux/Jetson version)."""
    if intent == "OPEN_CALCULATOR":
        try:
            subprocess.Popen(["gnome-calculator"])
            return True, "Calculator opened successfully."
        except Exception as e:
            return False, f"Could not open Calculator: {e}"
    elif intent == "OPEN_BROWSER":
        try:
            subprocess.Popen(["xdg-open", "https://www.google.com"])
            return True, "Browser opened successfully."
        except Exception as e:
            return False, f"Could not open Browser: {e}"
    elif intent == "OPEN_TEXT_EDITOR":
        try:
            subprocess.Popen(["gedit"])
            return True, "Text editor opened successfully."
        except Exception as e:
            return False, f"Could not open Text Editor: {e}"
    elif intent == "SCROLL_UP":
        try:
            subprocess.Popen(["xdotool", "click", "4"])
            return True, "Scrolled up."
        except Exception as e:
            return False, f"Could not scroll up: {e}"
    elif intent == "SCROLL_DOWN":
        try:
            subprocess.Popen(["xdotool", "click", "5"])
            return True, "Scrolled down."
        except Exception as e:
            return False, f"Could not scroll down: {e}"
    elif intent == "CLOSE_APPLICATION":
        try:
            subprocess.Popen(["xdotool", "getactivewindow", "windowkill"])
            return True, "Active application closed."
        except Exception as e:
            return False, f"Could not close application: {e}"
    elif intent == "OPEN_FILE_EXPLORER":
        try:
            subprocess.Popen(["nautilus"])
            return True, "File Explorer opened successfully."
        except Exception as e:
            return False, f"Could not open File Explorer: {e}"
    elif intent == "TAKE_SCREENSHOT":
        try:
            subprocess.run(["gnome-screenshot", "-f", "screenshot.png"])
            return True, "Screenshot saved as screenshot.png."
        except Exception as e:
            return False, f"Could not take screenshot: {e}"
    elif intent == "VOLUME_UP":
        try:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
            return True, "Volume increased."
        except Exception as e:
            return False, f"Could not increase volume: {e}"
    elif intent == "VOLUME_DOWN":
        try:
            subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
            return True, "Volume decreased."
        except Exception as e:
            return False, f"Could not decrease volume: {e}"
    else:
        return False, "Unknown or unsupported intent. No action taken."