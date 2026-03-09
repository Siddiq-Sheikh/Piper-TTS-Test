# Piper-TTS-Test
# 🔊 Piper Local TTS — Arabic & English Streaming

A lightweight Python script that runs **offline, local text-to-speech** using the [Piper](https://github.com/rhasspy/piper) C++ binary. Supports high-quality Arabic (Jordanian) and English (US) voices with real-time audio streaming — no cloud APIs, no API keys, no latency.

---

## ✨ Features

- **100% offline** — all synthesis happens on your machine
- **Streams audio in real time** via `sounddevice` — no waiting for full file generation
- **Arabic support** — uses the `ar_JO-kareem-medium` voice, the highest-quality Arabic model available for Piper
- **English support** — uses the `en_US-lessac-medium` voice
- **Auto-downloads** the Piper Windows binary and voice models on first run
- **Tashkeel (vowel diacritics) support** for more natural Arabic pronunciation

---

## 🖥️ Requirements

- **OS:** Windows (x64) — uses the prebuilt `piper_windows_amd64` binary
- **Python:** 3.8+

### Python Dependencies

```bash
pip install numpy sounddevice
```

> `os`, `json`, `urllib.request`, `zipfile`, and `subprocess` are all part of the Python standard library.

---

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/piper-local-tts.git
   cd piper-local-tts
   ```

2. **Install dependencies**
   ```bash
   pip install numpy sounddevice
   ```

3. **Run the script**
   ```bash
   python tts.py
   ```

On first run, the script will automatically:
- Download the Piper Windows binary (~8 MB)
- Download the Arabic Kareem Medium voice model (~60 MB)

Subsequent runs use the locally cached files.

---

## 🗣️ Switching Languages

Open `tts.py` and edit the `__main__` block:

**Arabic (default):**
```python
MODEL_FILE = download_model_arab("ar_JO-kareem-medium")
TEXT = "مَرْحَبًا بِكُمْ فِي عَالَمِ الذَّكَاءِ الاِصْطِنَاعِيِّ."
stream_tts(TEXT, PIPER_EXE, MODEL_FILE)
```

**English:**
```python
MODEL_FILE = download_piper_model_eng("en_US-lessac-medium")
TEXT = "Hello! This is local, offline text to speech running at full speed."
stream_tts(TEXT, PIPER_EXE, MODEL_FILE)
```

---

## 📁 Project Structure

```
piper-local-tts/
├── tts.py                          # Main script
├── piper_bin/                      # Auto-created: Piper C++ binary
│   └── piper/
│       └── piper.exe
├── ar_JO-kareem-medium.onnx        # Auto-downloaded: Arabic voice model
├── ar_JO-kareem-medium.onnx.json   # Auto-downloaded: Arabic voice config
├── en_US-lessac-medium.onnx        # Auto-downloaded: English voice model
└── en_US-lessac-medium.onnx.json   # Auto-downloaded: English voice config
```

---

## ⚙️ How It Works

1. The Piper C++ executable is launched as a subprocess with `--output_raw`
2. Text is piped to its `stdin`
3. Raw 16-bit PCM audio is read from `stdout` in 4096-byte chunks
4. Each chunk is written directly to a `sounddevice.OutputStream` for real-time playback

This approach bypasses Python's TTS ecosystem entirely, using Piper's highly optimized native binary for speed and reliability.

---

## 🌍 Available Voices

Piper supports many languages and voices. Browse the full list at the [Piper Voices repo](https://huggingface.co/rhasspy/piper-voices).

To add a new voice, create a download function following the pattern of `download_model_arab()` or `download_piper_model_eng()`, pointing to the correct HuggingFace path for your language and speaker.

---

## 📄 License

This project is released under the **MIT License**.

Piper itself is licensed under the [MIT License](https://github.com/rhasspy/piper/blob/master/LICENSE).  
Voice models are distributed by [Rhasspy](https://huggingface.co/rhasspy/piper-voices) under their respective licenses.

---

## 🙏 Acknowledgements

- [Piper TTS](https://github.com/rhasspy/piper) by Rhasspy — the incredible offline TTS engine powering this project
- [Kareem voice model](https://huggingface.co/rhasspy/piper-voices) — Jordanian Arabic, medium quality
