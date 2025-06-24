import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import glob
import os
import whisper
import numpy as np
from jiwer import wer, cer

fs = 16000

def record_audio(seconds=180, recording_folder="recordings"):
    os.makedirs(recording_folder, exist_ok=True)
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    nonzero = np.flatnonzero(np.abs(audio) > 0)
    actual_frames = nonzero[-1] + 1 if len(nonzero) > 0 else 0
    audio_trimmed = audio[:actual_frames]
    duration_seconds = len(audio_trimmed) / fs
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"recording_{timestamp}.wav"
    filepath = os.path.join(recording_folder, filename)
    write(filepath, fs, audio_trimmed)
    return filepath, duration_seconds

def transcribe_audio(filepath, transcription_folder="transcriptions"):
    os.makedirs(transcription_folder, exist_ok=True)
    model = whisper.load_model("base")
    result = model.transcribe(filepath)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    transcription_filename = f"transcription_{timestamp}.txt"
    transcription_filepath = os.path.join(transcription_folder, transcription_filename)
    with open(transcription_filepath, "w", encoding="utf-8") as f:
        f.write(result["text"])
    return result["text"]

def scan_transcription(reference, hypothesis, duration_seconds=0, scan_folder="scan_results"):
    os.makedirs(scan_folder, exist_ok=True)
    word_error = wer(reference, hypothesis)
    char_error = cer(reference, hypothesis)
    result = (
        f"reference: '{reference}'\n"
        f"spoken: '{hypothesis}'\n"
        f"Word Error Rate (WER): {word_error:.2%}\n"
        f"Character Error Rate (CER): {char_error:.2%}\n"
    )
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"scan_result_{timestamp}.txt"
    filepath = os.path.join(scan_folder, filename)
    with open(filepath, "w", encoding="utf-8") as out:
        out.write(result)
    return result, filename