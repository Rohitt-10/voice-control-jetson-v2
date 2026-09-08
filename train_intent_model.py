import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ============================================
# LOAD DATASET
# ============================================

DATASET_PATH = "dataset/commands.csv"

df = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully")
print("Total examples:", len(df))
print("Total intents:", df["intent"].nunique())


# ============================================
# SPLIT DATA
# ============================================

X = df["text"]
y = df["intent"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))


# ============================================
# CREATE ML PIPELINE
# ============================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# ============================================
# TRAIN MODEL
# ============================================

print("\n[INFO] Training ML model...")

model.fit(X_train, y_train)

print("[INFO] Training completed.")


# ============================================
# TEST MODEL
# ============================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n============================================")
print("MODEL RESULTS")
print("============================================")

print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# ============================================
# SAVE MODEL
# ============================================

MODEL_PATH = r"intent_model.pkl"

joblib.dump(model, MODEL_PATH)

print("============================================")
print(f"[SUCCESS] Model saved as: {MODEL_PATH}")
print("============================================")