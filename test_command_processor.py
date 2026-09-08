from command_processor import process_command

tests = [
    "open calculator",
    "open the browser",
    "scroll up",
    "take a screenshot",
    "tell me a joke"
]

for t in tests:
    print(t, "->", process_command(t))