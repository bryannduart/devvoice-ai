const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");
const transcriptionEl = document.getElementById("transcription");

let mediaRecorder;
let audioChunks = [];
let stream;

startBtn.addEventListener("click", async () => {
  try {
    transcriptionEl.textContent = "---";
    statusText.textContent = "Status: solicitando acesso ao microfone...";

    stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioChunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstart = () => {
      statusText.textContent = "Status: gravando...";
      startBtn.disabled = true;
      stopBtn.disabled = false;
    };

    mediaRecorder.onstop = async () => {
      statusText.textContent = "Status: enviando áudio para transcrição...";

      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      try {
        const response = await fetch("http://127.0.0.1:8000/transcribe", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Erro ao transcrever áudio.");
        }

        transcriptionEl.textContent = data.transcription;
        statusText.textContent = "Status: transcrição concluída.";
      } catch (error) {
        transcriptionEl.textContent = "---";
        statusText.textContent = `Erro: ${error.message}`;
      } finally {
        startBtn.disabled = false;
        stopBtn.disabled = true;

        if (stream) {
          stream.getTracks().forEach((track) => track.stop());
        }
      }
    };

    mediaRecorder.start();
  } catch (error) {
    statusText.textContent = `Erro ao acessar o microfone: ${error.message}`;
  }
});

stopBtn.addEventListener("click", () => {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
});