import joblib

model = joblib.load("intent_model.pkl")

test_texts = ["scroll down", "volume up", "volume down"]

for text in test_texts:
    probabilities = model.predict_proba([text])[0]
    best_index = probabilities.argmax()
    best_prob = probabilities[best_index]
    predicted_intent = model.classes_[best_index]
    print(f"{text!r} -> {predicted_intent} (confidence: {best_prob:.3f})")