import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import sys

DEVICE_INDEX = 1
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
WAKE_MODEL = r"C:\Users\rohit\voice_control\venv\Lib\site-packages\openwakeword\resources\models\hey_jarvis_v0.1.onnx"
THRESHOLD = 0.5
COOLDOWN_FRAMES = 30


def main():
    print("[INFO] Loading wake word model...")

    try:
        oww_model = Model(
            wakeword_models=[WAKE_MODEL],
            inference_framework="onnx"
        )
    except Exception as e:
        print(f"[ERROR] Could not load model: {e}")
        sys.exit(1)

    cooldown = 0
    print("[READY] Waiting for wake word...")

    def callback(indata, frames, time_info, status):
        nonlocal cooldown

        if status:
            print(f"[WARNING] {status}")

        audio_chunk = indata[:, 0].astype(np.int16)

        try:
            prediction = oww_model.predict(audio_chunk)
        except Exception as e:
            print(f"[ERROR] Prediction failed: {e}")
            return

        if cooldown > 0:
            cooldown -= 1
            return

        for model_name, score in prediction.items():
            if score > THRESHOLD:
                print(
                    f"[WAKE WORD] Detected! "
                    f"{model_name}: {score:.2f}"
                )
                cooldown = COOLDOWN_FRAMES
                break

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=CHUNK_SIZE,
            device=DEVICE_INDEX,
            callback=callback
        ):
            while True:
                sd.sleep(100)

    except KeyboardInterrupt:
        print("\n[INFO] Stopped cleanly by user.")

    except Exception as e:
        print(f"[ERROR] Audio stream failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()