import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI

load_dotenv(override=True)

app = FastAPI(title="DevVoice AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def read_root():
    return {
        "message": "DevVoice AI backend online"
    }


@app.get("/health")
def health_check():
    api_key_loaded = bool(os.getenv("OPENAI_API_KEY"))

    return {
        "status": "ok",
        "openai_key_loaded": api_key_loaded
    }


@app.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Recebe um arquivo de áudio enviado pelo frontend,
    salva temporariamente e envia para transcrição.
    """

    suffix = Path(audio.filename).suffix if audio.filename else ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(await audio.read())
        temp_audio_path = temp_audio.name

    try:
        with open(temp_audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        return JSONResponse({
            "transcription": transcription.text
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)