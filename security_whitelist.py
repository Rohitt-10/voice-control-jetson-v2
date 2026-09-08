ALLOWED_INTENTS = {
    "OPEN_CALCULATOR",
    "OPEN_BROWSER",
    "OPEN_TEXT_EDITOR",
    "SCROLL_UP",
    "SCROLL_DOWN",
    "CLOSE_APPLICATION",
    "OPEN_FILE_EXPLORER",
    "TAKE_SCREENSHOT",
    "VOLUME_UP",
    "VOLUME_DOWN"
}

def is_intent_allowed(intent):
    """
    Check whether an intent is explicitly allowed
    to perform a computer action.
    """
    return intent in ALLOWED_INTENTS

if __name__ == "__main__":
    test_intents = [
        "OPEN_CALCULATOR",
        "OPEN_BROWSER",
        "OPEN_TEXT_EDITOR",
        "SCROLL_UP",
        "SCROLL_DOWN",
        "CLOSE_APPLICATION",
        "OPEN_FILE_EXPLORER",
        "TAKE_SCREENSHOT",
        "VOLUME_UP",
        "VOLUME_DOWN",
        "UNKNOWN"
    ]
    for intent in test_intents:
        if is_intent_allowed(intent):
            print(f"[ALLOWED] {intent}")
        else:
            print(f"[REJECTED] {intent}")