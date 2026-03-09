import os
import json
import urllib.request
import zipfile
import subprocess
import numpy as np
import sounddevice as sd

def setup_piper():
    """Downloads the completely standalone Piper C++ binary for Windows."""
    piper_dir = "piper_bin"
    exe_path = os.path.join(piper_dir, "piper", "piper.exe")
    
    if not os.path.exists(exe_path):
        print("Downloading the bulletproof Piper Windows binary...")
        zip_url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip"
        zip_path = "piper.zip"
        urllib.request.urlretrieve(zip_url, zip_path)
        
        print("Extracting Piper...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(piper_dir)
        os.remove(zip_path)
        print("Piper binary ready.")
        
    return exe_path

def download_model_arab(model_prefix="ar_JO-kareem-medium"):
    """Downloads the Arabic Kareem model."""
    # Updated URL for Arabic Kareem Medium
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/medium/"
    onnx_file = f"{model_prefix}.onnx"
    json_file = f"{model_prefix}.onnx.json"
    
    if not os.path.exists(onnx_file):
        print(f"Downloading model {onnx_file}...")
        urllib.request.urlretrieve(base_url + onnx_file, onnx_file)
    if not os.path.exists(json_file):
        print(f"Downloading config {json_file}...")
        urllib.request.urlretrieve(base_url + json_file, json_file)
        
    return onnx_file

def download_piper_model_eng(model_prefix="en_US-lessac-medium"):
    """Downloads the .onnx and .json files if they don't exist locally."""
    base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/"
    onnx_file = f"{model_prefix}.onnx"
    json_file = f"{model_prefix}.onnx.json"
    
    if not os.path.exists(onnx_file):
        print(f"Downloading {onnx_file}...")
        urllib.request.urlretrieve(base_url + onnx_file, onnx_file)
    if not os.path.exists(json_file):
        print(f"Downloading {json_file}...")
        urllib.request.urlretrieve(base_url + json_file, json_file)
        
    return onnx_file

def stream_tts(text, piper_exe, model_path):
    print(f"\nSynthesizing: '{text}'")
    
    # Read sample rate from config
    with open(model_path + ".json", 'r', encoding='utf-8') as f:
        config = json.load(f)
    sample_rate = config['audio']['sample_rate']
    
    # Launch the highly-optimized C++ executable
    cmd = [piper_exe, "--model", model_path, "--output_raw"]
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL 
    )
    
    # Send text and close stdin
    process.stdin.write(text.encode('utf-8'))
    process.stdin.close()
    
    print("Opening audio stream...")
    stream = sd.OutputStream(samplerate=sample_rate, channels=1, dtype='int16')
    stream.start()
    
    audio_played = False
    while True:
        raw_audio = process.stdout.read(4096)
        if not raw_audio:
            break 
        
        audio_chunk = np.frombuffer(raw_audio, dtype=np.int16)
        stream.write(audio_chunk)
        audio_played = True
        
    stream.stop()
    stream.close()
    process.wait()
    
    if not audio_played:
        print("\nError: The binary failed to generate audio.")
    else:
        print("\nDone playing!")

if __name__ == "__main__":
    PIPER_EXE = setup_piper()
    
    # Switched to Kareem Medium (The best Arabic model available for Piper)
    MODEL_FILE = download_model_arab("ar_JO-kareem-medium")
    
    # Arabic text with Tashkeel (vowels) for much higher realism
    TEXT = "مَرْحَبًا بِكُمْ فِي عَالَمِ الذَّكَاءِ الاِصْطِنَاعِيِّ. أَنَا كَرِيم، أَسْرَعُ صَوْتٍ عَرَبِيٍّ مَحَلِّيٍّ."

    # TEXT = (
    #     "Listen to me carefully. The Python package is dead on Windows. "
    #     "This is the raw binary working flawlessly, streaming directly "
    #     "to your speakers without any silent failures."
    # )
    
    stream_tts(TEXT, PIPER_EXE, MODEL_FILE)