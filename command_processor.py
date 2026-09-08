import joblib

MODEL_PATH = "intent_model.pkl"
CONFIDENCE_THRESHOLD = 0.25

_model = joblib.load(MODEL_PATH)

def process_command(text):
    text = text.strip()

    if not text:
        return {"intent": "UNKNOWN", "text": text}

    probabilities = _model.predict_proba([text])[0]
    best_index = probabilities.argmax()
    best_prob = probabilities[best_index]
    predicted_intent = _model.classes_[best_index]

    if best_prob < CONFIDENCE_THRESHOLD:
        return {"intent": "UNKNOWN", "text": text}

    return {"intent": predicted_intent, "text": text}