import re


# Each intent maps to a list of trigger phrases.
# Matching is done by checking whether any trigger phrase appears
# as a substring of the normalized input text.
INTENT_PATTERNS = {
    "OPEN_CALCULATOR": [
        "open calculator", "launch calculator", "start calculator",
        "open the calculator", "launch the calculator", "start the calculator",
    ],
    "OPEN_BROWSER": [
        "open browser", "launch browser", "start browser",
        "open the browser", "launch the browser", "start the browser",
    ],
    "OPEN_TEXT_EDITOR": [
        "open text editor", "open editor", "launch text editor",
        "launch editor", "start text editor", "start editor",
        "open the text editor", "open the editor",
    ],
    "SCROLL_UP": [
        "scroll up", "move up", "go up",
    ],
    "SCROLL_DOWN": [
        "scroll down", "move down", "go down",
    ],
    "CLOSE_APPLICATION": [
        "close application", "close app", "exit application",
        "close the application", "close the app", "exit the application",
    ],
}


def normalize_text(text):
    """Lowercase, strip, collapse whitespace, remove punctuation."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text)       # collapse multiple spaces
    return text


def process_command(text):
    """
    Convert recognized speech text into a structured intent result.

    Returns a dict:
        {
            "intent": str,
            "confidence": float,   # heuristic score, NOT an ML probability
            "original_text": str
        }
    """
    original_text = text
    normalized = normalize_text(text)

    if not normalized:
        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "original_text": original_text,
        }

    best_intent = "UNKNOWN"
    best_score = 0.0

    for intent, phrases in INTENT_PATTERNS.items():
        for phrase in phrases:
            if phrase in normalized:
                # Heuristic score: longer matched phrase relative to the
                # full input = higher confidence. This is a simple ratio,
                # not a statistical/ML confidence value.
                score = len(phrase) / len(normalized)
                score = min(score, 1.0)
                # Prefer exact full-text matches strongly
                if normalized == phrase:
                    score = 1.0
                if score > best_score:
                    best_score = score
                    best_intent = intent

    if best_intent == "UNKNOWN":
        return {
            "intent": "UNKNOWN",
            "confidence": 0.0,
            "original_text": original_text,
        }

    return {
        "intent": best_intent,
        "confidence": round(best_score, 2),
        "original_text": original_text,
    }


if __name__ == "__main__":
    # Quick manual check when running this file directly
    samples = [
        "open calculator",
        "please open the calculator",
        "launch calculator",
        "open browser",
        "scroll up",
        "move down",
        "close application",
        "tell me a joke",
    ]
    for s in samples:
        print(s, "->", process_command(s))