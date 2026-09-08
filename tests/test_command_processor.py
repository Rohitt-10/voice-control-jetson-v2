import sys
import os

# Allow importing command_processor.py from the parent folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from command_processor import process_command


TEST_CASES = [
    ("open calculator", "OPEN_CALCULATOR"),
    ("launch calculator", "OPEN_CALCULATOR"),
    ("please open the calculator", "OPEN_CALCULATOR"),
    ("open browser", "OPEN_BROWSER"),
    ("launch browser", "OPEN_BROWSER"),
    ("open editor", "OPEN_TEXT_EDITOR"),
    ("scroll up", "SCROLL_UP"),
    ("move up", "SCROLL_UP"),
    ("scroll down", "SCROLL_DOWN"),
    ("move down", "SCROLL_DOWN"),
    ("close application", "CLOSE_APPLICATION"),
    ("close app", "CLOSE_APPLICATION"),
    ("tell me a joke", "UNKNOWN"),
    ("hello", "UNKNOWN"),
    ("random text", "UNKNOWN"),
]


def run_tests():
    passed = 0
    failed = 0

    for text, expected_intent in TEST_CASES:
        result = process_command(text)
        actual_intent = result["intent"]

        status = "PASS" if actual_intent == expected_intent else "FAIL"

        if status == "PASS":
            passed += 1
        else:
            failed += 1

        print(
            f"[{status}] '{text}' -> "
            f"expected {expected_intent}, got {actual_intent} "
            f"(confidence={result['confidence']})"
        )

    print(
        f"\n{passed} passed, {failed} failed "
        f"out of {len(TEST_CASES)} tests"
    )


if __name__ == "__main__":
    run_tests()