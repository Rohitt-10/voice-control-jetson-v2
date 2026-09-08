import joblib

MODEL_PATH = "intent_model.pkl"

print("============================================")
print(" ML INTENT MODEL TEST")
print("============================================")

model = joblib.load(MODEL_PATH)

print("[INFO] ML model loaded successfully.")
print()

test_commands = [
    "Could you open the calculator for me?",
    "Please bring up the web browser",
    "I want to open my files",
    "Can you start the text editor?",
    "Move the page upward",
    "Move the page downward",
    "Please close the current application",
    "Capture the screen",
    "Make the volume louder",
    "Reduce the volume",
    "Show me the calculator",
    "Can you take a screenshot?"
]

print("PREDICTIONS")
print("--------------------------------------------")

for command in test_commands:
    prediction = model.predict([command])[0]
    print(f"{command}")
    print(f"   -> {prediction}")
    print()

print("============================================")
print(" TEST COMPLETED")
print("============================================")