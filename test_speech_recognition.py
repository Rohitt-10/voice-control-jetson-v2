import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import sys
import time

# ---- CONFIG ----
DEVICE_INDEX = None        # Set to your mic's index if default is wrong
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5          # Fixed recording window for this standalone test
MODEL_SIZE = "base"           # tiny / base / small / medium / large-v3 — base is a good CPU starting point
COMPUTE_TYPE = "int8"          # int8 is fastest and most memory-efficient on CPU


def load_model():
    print(f"[INFO] Loading Whisper model '{MODEL_SIZE}' (this happens once)...")
    try:
        model = WhisperModel(MODEL_SIZE, device="cpu", compute_type=COMPUTE_TYPE)
    except Exception as e:
        print(f"[ERROR] Could not load model: {e}")
        sys.exit(1)
    print("[INFO] Model loaded.")
    return model


def record_audio():
    print(f"[LISTENING] Speak your command ({RECORD_SECONDS}s)...")
    try:
        audio = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='float32',
            device=DEVICE_INDEX
        )
        sd.wait()
    except Exception as e:
        print(f"[ERROR] Recording failed: {e}")
        sys.exit(1)
    return audio.flatten()


def transcribe(model, audio):
    print("[INFO] Transcribing...")
    start = time.time()
    try:
        segments, info = model.transcribe(audio, language="en", beam_size=5)
        text = " ".join(segment.text.strip() for segment in segments)
    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return None
    elapsed = time.time() - start
    print(f"[INFO] Transcription took {elapsed:.2f}s")
    return text.strip()


def main():
    model = load_model()
    try:
        while True:
            input("\nPress Enter to record a 5-second command (Ctrl+C to quit)...")
            audio = record_audio()
            text = transcribe(model, audio)
            if text:
                print(f"[STT] {text}")
            else:
                print("[STT] (no speech recognized)")
    except KeyboardInterrupt:
        print("\n[INFO] Stopped cleanly by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()