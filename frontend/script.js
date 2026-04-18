const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");
const transcriptionEl = document.getElementById("transcription");
const responseTextEl = document.getElementById("responseText");
const responseAudioEl = document.getElementById("responseAudio");

let mediaRecorder;
let audioChunks = [];
let stream;

startBtn.addEventListener("click", async () => {
  try {
    transcriptionEl.textContent = "---";
    responseTextEl.textContent = "---";
    responseAudioEl.src = "";
    statusText.textContent = "Solicitando acesso ao microfone...";

    stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioChunks = [];
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstart = () => {
      statusText.textContent = "Gravando sua pergunta...";
      startBtn.disabled = true;
      stopBtn.disabled = false;
    };

    mediaRecorder.onstop = async () => {
      statusText.textContent = "Enviando áudio para o DevVoice AI...";

      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      try {
        const response = await fetch("http://127.0.0.1:8000/ask", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Erro ao processar áudio.");
        }

        transcriptionEl.textContent = data.transcription;
        responseTextEl.textContent = data.response_text;

        const audioSrc = `data:${data.audio_mime_type};base64,${data.response_audio_base64}`;
        responseAudioEl.src = audioSrc;

        try {
          await responseAudioEl.play();
        } catch {
        }

        statusText.textContent = "Resposta concluída com sucesso.";
      } catch (error) {
        transcriptionEl.textContent = "---";
        responseTextEl.textContent = "---";
        responseAudioEl.src = "";
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