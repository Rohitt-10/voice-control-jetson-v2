import sys
import time
from datetime import datetime

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from openwakeword.model import Model

from command_processor import process_command
from computer_control_linux import execute_intent
from security_whitelist import is_intent_allowed


# ============================================================
# CONFIGURATION
# ============================================================

DEVICE_INDEX = 1
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280

COMMAND_SECONDS = 5

WAKE_THRESHOLD = 0.5
COOLDOWN_SECONDS = 2.0

WAKE_MODEL = (
    r"C:\Users\rohit\voice_control\venv\Lib\site-packages"
    r"\openwakeword\resources\models\hey_jarvis_v0.1.onnx"
)

WHISPER_MODEL_SIZE = "base"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"


# ============================================================
# LOGGING
# ============================================================

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("assistant_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


# ============================================================
# LOAD WAKE WORD MODEL
# ============================================================

def load_wake_word_model():
    print("[INFO] Loading wake-word model...")

    try:
        model = Model(
            wakeword_models=[WAKE_MODEL],
            inference_framework="onnx"
        )

        print("[INFO] Wake-word model loaded.")
        return model

    except Exception as e:
        print(f"[ERROR] Could not load wake-word model: {e}")
        sys.exit(1)


# ============================================================
# LOAD WHISPER
# ============================================================

def load_whisper_model():
    print("[INFO] Loading Whisper model...")

    try:
        model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE
        )

        print("[INFO] Whisper model loaded.")
        return model

    except Exception as e:
        print(f"[ERROR] Could not load Whisper model: {e}")
        sys.exit(1)


# ============================================================
# WAIT FOR WAKE WORD
# ============================================================

def wait_for_wake_word(wake_model):

    print("[READY] Waiting for wake word...")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=CHUNK_SIZE,
            device=DEVICE_INDEX
        ) as stream:

            while True:

                audio_chunk, overflowed = stream.read(CHUNK_SIZE)

                if overflowed:
                    print("[WARNING] Audio buffer overflow.")

                audio_chunk = audio_chunk[:, 0]

                prediction = wake_model.predict(audio_chunk)

                for model_name, score in prediction.items():

                    if score >= WAKE_THRESHOLD:
                        print(
                            f"[WAKE WORD] Detected! "
                            f"{model_name}: {score:.2f}"
                        )

                        return True

    except KeyboardInterrupt:
        raise

    except Exception as e:
        print(f"[ERROR] Wake-word stream failed: {e}")
        return False


# ============================================================
# RECORD COMMAND
# ============================================================

def record_command():

    print(
        f"[LISTENING] Speak your command "
        f"within {COMMAND_SECONDS} seconds..."
    )

    try:
        audio = sd.rec(
            int(COMMAND_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            device=DEVICE_INDEX
        )

        sd.wait()

        audio = audio.flatten()

        if len(audio) == 0:
            print("[WARNING] No audio captured.")
            return None

        max_amplitude = np.max(np.abs(audio))

        if max_amplitude < 0.001:
            print("[WARNING] Audio seems silent.")
            return None

        return audio

    except Exception as e:
        print(f"[ERROR] Command recording failed: {e}")
        return None


# ============================================================
# SPEECH TO TEXT
# ============================================================

def transcribe_command(whisper_model, audio):

    print("[INFO] Transcribing...")

    try:
        segments, info = whisper_model.transcribe(
            audio,
            language="en",
            beam_size=5,
            vad_filter=True
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        ).strip()

        if text:
            print(f"[STT] {text}")
        else:
            print("[STT] No speech recognized.")

        return text

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return ""


# ============================================================
# HANDLE COMMAND (PROCESS -> SECURITY -> EXECUTE)
# ============================================================

def handle_command(text):

    result = process_command(text)
    intent = result["intent"]

    print(f"[INTENT] {intent}")
    log_event(f"Command text: '{text}' | Intent: {intent}")

    if intent == "UNKNOWN":
        print("[SECURITY] No valid intent recognized.")
        print("[ACTION] No action taken.")
        log_event("Result: REJECTED (unknown intent)")
        return

    if not is_intent_allowed(intent):
        print(f"[SECURITY] Intent '{intent}' is not on the whitelist.")
        print("[ACTION] No action taken.")
        log_event(f"Result: REJECTED (not on whitelist) - {intent}")
        return

    print(f"[SECURITY] Intent '{intent}' approved.")

    try:
        success, message = execute_intent(intent)

        if success:
            print(f"[ACTION] Executing {intent}...")
            print(f"[SUCCESS] {message}")
            log_event(f"Result: SUCCESS - {message}")
        else:
            print(f"[ERROR] {message}")
            log_event(f"Result: FAILED - {message}")

    except Exception as e:
        print(f"[ERROR] Execution failed: {e}")
        log_event(f"Result: EXCEPTION - {e}")


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print("==========================================")
    print(" Wake-Word Voice Assistant")
    print("==========================================")

    wake_model = load_wake_word_model()
    whisper_model = load_whisper_model()

    last_detection_time = 0

    try:

        while True:

            detected = wait_for_wake_word(wake_model)

            if not detected:
                continue

            current_time = time.time()

            if current_time - last_detection_time < COOLDOWN_SECONDS:
                continue

            last_detection_time = current_time

            audio = record_command()

            if audio is None:
                print("[READY] Returning to wake-word mode...")
                continue

            text = transcribe_command(
                whisper_model,
                audio
            )

            if not text:
                print("[READY] Returning to wake-word mode...")
                continue

            handle_command(text)

            print("[READY] Returning to wake-word mode...")

    except KeyboardInterrupt:

        print("\n[INFO] Stopped cleanly by user.")
        sys.exit(0)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()