let mediaRecorder;
let audioChunks = [];
const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const audioPlayback = document.getElementById('audioPlayback');
const audiofileInput = document.getElementById('audiofile');

if (recordBtn && stopBtn && audioPlayback && audiofileInput) {
    recordBtn.onclick = async function() {
        audioChunks = [];
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();
        recordBtn.disabled = true;
        stopBtn.disabled = false;

        mediaRecorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };
        mediaRecorder.onstop = e => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const audioUrl = URL.createObjectURL(audioBlob);
            audioPlayback.src = audioUrl;
            audioPlayback.style.display = 'block';

            // Overwrite file input with recorded audio
            const file = new File([audioBlob], "recording.wav", { type: "audio/wav" });
            const dt = new DataTransfer();
            dt.items.add(file);
            audiofileInput.files = dt.files;
        };
    };

    stopBtn.onclick = function() {
        mediaRecorder.stop();
        recordBtn.disabled = false;
        stopBtn.disabled = true;
    };
}