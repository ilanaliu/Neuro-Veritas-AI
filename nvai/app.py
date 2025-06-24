from flask import Flask, render_template, request, flash
import os
import glob
import numpy as np
from datetime import datetime
from ml.ai import transcribe_audio, scan_transcription
from scipy.io import wavfile
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "your_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_real_text():
    if os.path.exists("real.txt"):
        with open("real.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/research", methods=["GET", "POST"])
def research():
    transcription = ""
    scan_result = ""
    real_text = load_real_text()
    filename = None
    scan_filename = None
    if request.method == "POST":
        if "audiofile" in request.files:
            file = request.files["audiofile"]
            if file and file.filename.endswith(".wav"):
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"audio_{timestamp}.wav"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                flash(f"Audio uploaded: {file.filename}", "success")

                transcription = transcribe_audio(filepath)
                reference = request.form.get("reference", "").strip()
                if reference:
                    scan_result, scan_filename = scan_transcription(reference, transcription)
                else:
                    scan_filename = None
                flash("Transcription and scan complete.", "success")
            else:
                flash("Please upload a .wav file.", "danger")
    return render_template(
        "research.html",
        transcription=transcription,
        scan_result=scan_result,
        real_text=real_text,
        audio_filename=filename,
        scan_filename=scan_filename,
    )
    return render_template(
        "research.html",
        transcription=transcription,
        scan_result=scan_result,
        real_text=real_text,
        audio_filename=filename,
        scan_filename=scan_filename,
    )

@app.route("/mission")
def mission():
    return render_template("mission.html")

@app.route('/uploads/<filename>')
def download_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/scan_results/<filename>')
def download_scan(filename):
    return send_from_directory('scan_results', filename, as_attachment=True)

@app.route('/recordings/<filename>')
def download_recording(filename):
    return send_from_directory('recordings', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)