import os

os.environ.setdefault("HF_HUB_ETAG_TIMEOUT", "60")
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "60")

import torch
import torchaudio

from generator import DEFAULT_MISO_TTS_REPO_ID, load_miso_8b

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

generator = load_miso_8b(device, model_path_or_repo_id=DEFAULT_MISO_TTS_REPO_ID)

text = "Hello from Miso, running locally on a MacBook."
print(f"Generating: {text}")
audio = generator.generate(text=text, speaker=0, context=[], max_audio_length_ms=8_000)

torchaudio.save("short_sentence.wav", audio.unsqueeze(0).cpu(), generator.sample_rate)
print("Wrote short_sentence.wav")
