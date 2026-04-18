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

SYSTEM_PROMPT = """
Você é o DevVoice AI, um assistente virtual focado em programação,
aprendizado de tecnologia e evolução como desenvolvedor.

Seu papel:
- responder como um mentor técnico paciente e didático
- explicar de forma clara e organizada
- ajudar iniciantes e intermediários
- usar linguagem simples quando necessário
- quando fizer sentido, responder em passos
- quando falar de código, usar exemplos curtos e práticos
- evitar respostas exageradamente longas
- manter um tom profissional, amigável e objetivo
"""


@app.get("/")
def read_root():
    return {
        "message": "DevVoice AI backend online"
    }


@app.get("/health")
def health_check():
    api_key = os.getenv("OPENAI_API_KEY")
    api_key_loaded = bool(api_key)

    masked_key = None
    if api_key_loaded and len(api_key) > 10:
        masked_key = f"{api_key[:7]}...{api_key[-4:]}"
    elif api_key_loaded:
        masked_key = "key_loaded_but_too_short"

    return {
        "status": "ok",
        "openai_key_loaded": api_key_loaded,
        "openai_key_preview": masked_key
    }


@app.post("/ask")
async def ask_devvoice(audio: UploadFile = File(...)):
    """
    Recebe um áudio, transcreve e gera uma resposta da IA.
    """
    suffix = Path(audio.filename).suffix if audio.filename else ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        temp_audio.write(await audio.read())
        temp_audio_path = temp_audio.name

    try:
        # 1. Transcrição do áudio
        with open(temp_audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )

        user_text = transcription.text.strip()

        # 2. Resposta da IA
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        answer_text = response.output_text.strip()

        return JSONResponse({
            "transcription": user_text,
            "response_text": answer_text
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)