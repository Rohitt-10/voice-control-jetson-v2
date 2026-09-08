from voice_assistant import handle_command

test_texts = [
    "open calculator",
    "open the browser",
    "open the text editor",
    "scroll up",
    "scroll down",
    "close application",
    "open file explorer",
    "take a screenshot",
    "volume up",
    "volume down",
    "tell me a joke"
]

for text in test_texts:
    print(f"\n--- Command: {text} ---")
    handle_command(text)
