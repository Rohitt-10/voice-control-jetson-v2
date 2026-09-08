from computer_control import execute_intent

for intent in ["OPEN_FILE_EXPLORER", "TAKE_SCREENSHOT", "VOLUME_UP", "VOLUME_DOWN"]:
    result = execute_intent(intent)
    print(intent, "->", result)