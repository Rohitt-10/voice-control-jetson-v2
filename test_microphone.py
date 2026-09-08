import sounddevice as sd
import numpy as np
import wave
import sys

# ---- CONFIG ----
DEVICE_INDEX = 1   # Set to an integer (e.g. 1) if default device is wrong
SAMPLE_RATE = 16000    # 16kHz is standard for speech processing
CHANNELS = 1            # Mono is sufficient for speech
DURATION = 5            # seconds
OUTPUT_FILE = "test.wav"


def record_audio():
    print("[INFO] Checking microphone...")
    try:
        device_info = sd.query_devices(DEVICE_INDEX, 'input')
        print(f"[INFO] Microphone detected: {device_info['name']}")
    except Exception as e:
        print(f"[ERROR] Could not access microphone: {e}")
        sys.exit(1)

    print(f"[INFO] Recording for {DURATION} seconds... Speak now.")
    try:
        audio_data = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
            device=DEVICE_INDEX
        )
        sd.wait()  # Block until recording is finished
    except KeyboardInterrupt:
        print("\n[INFO] Recording stopped by user (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Recording failed: {e}")
        sys.exit(1)

    print("[INFO] Audio captured successfully")

    # Basic sanity check: is there actual signal, or just silence?
    max_amplitude = np.max(np.abs(audio_data))
    print(f"[INFO] Max amplitude in recording: {max_amplitude}")
    if max_amplitude < 100:
        print("[WARNING] Audio seems very quiet or silent. Check mic volume/permissions.")

    save_wav(audio_data)


def save_wav(audio_data):
    try:
        with wave.open(OUTPUT_FILE, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # int16 = 2 bytes
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_data.tobytes())
        print(f"[INFO] Saved audio file: {OUTPUT_FILE}")
    except Exception as e:
        print(f"[ERROR] Could not save WAV file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        record_audio()
    except KeyboardInterrupt:
        print("\n[INFO] Stopped cleanly by user.")
        sys.exit(0)