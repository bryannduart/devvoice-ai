# DevVoice AI

Assistente virtual por voz para programação, estudos e evolução como desenvolvedor.

O **DevVoice AI** é um projeto full stack que permite ao usuário gravar uma pergunta por voz, enviar esse áudio para processamento, obter uma resposta inteligente focada em programação e, por fim, receber essa resposta em **texto e voz**.

A proposta do projeto é demonstrar, na prática, a integração entre:

- captura de áudio no navegador
- transcrição de fala
- geração de resposta com IA
- síntese de voz
- comunicação entre frontend e backend

---

## Objetivo do projeto

O objetivo do **DevVoice AI** é servir como um mentor virtual por voz para estudantes e desenvolvedores iniciantes ou intermediários, ajudando com:

- dúvidas de programação
- explicações de conceitos técnicos
- orientação de estudos
- evolução como desenvolvedor
- aprendizado de tecnologia de forma mais interativa

Além do valor prático, o projeto também foi desenvolvido com foco em **portfólio**, demonstrando habilidades em frontend, backend, integração com APIs e experiência do usuário.

---

## Demonstração do fluxo

O fluxo principal do sistema funciona assim:

1. o usuário grava uma pergunta por voz no navegador
2. o frontend captura o áudio com o microfone
3. o áudio é enviado para o backend
4. o backend envia o áudio para transcrição
5. a transcrição é enviada para o modelo de IA
6. a IA gera uma resposta didática e objetiva
7. a resposta é convertida em áudio
8. o frontend exibe:
   - a transcrição
   - a resposta em texto
   - o player com a resposta em voz

---

## Funcionalidades

### Funcionalidades implementadas

- captura de áudio diretamente no navegador
- gravação com `MediaRecorder`
- envio do áudio para o backend com `fetch`
- backend em FastAPI
- endpoint para transcrição de áudio
- endpoint para resposta completa do assistente
- persona personalizada do DevVoice AI
- resposta técnica orientada para programação
- geração de áudio da resposta
- reprodução do áudio no frontend
- interface moderna com visual futurista
- integração frontend + backend

### Exemplos de uso

O usuário pode fazer perguntas como:

- “Explique o que é uma API.”
- “O que é um JOIN em SQL?”
- “Como aprender JavaScript do zero?”
- “Explique orientação a objetos de forma simples.”
- “Me diga como evoluir como desenvolvedor backend.”

---

## Tecnologias utilizadas

### Frontend
- HTML5
- CSS3
- JavaScript
- MediaRecorder API
- Fetch API

### Backend
- Python
- FastAPI
- Uvicorn
- python-dotenv
- python-multipart

### IA e áudio
- OpenAI API
- Speech-to-Text
- geração de resposta com modelo de linguagem
- Text-to-Speech

---

## Estrutura do projeto

```bash
devvoice-ai/
├── backend/
│   ├── venv/
│   ├── .env
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── README.md
└── LICENSE
```

---

## Arquitetura do projeto

O sistema foi dividido em duas camadas principais:

### Frontend
Responsável por capturar o áudio do usuário, enviar o arquivo para o backend e exibir a transcrição, a resposta em texto e o áudio retornado pelo assistente.

### Backend
Responsável por receber o áudio, processar a transcrição, gerar a resposta com IA, converter a resposta em voz e retornar os dados ao frontend.

---

## Como executar localmente

### Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/devvoice-ai.git
cd devvoice-ai
```

### Configurar o backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configurar a variável de ambiente

Crie o arquivo `.env` dentro da pasta `backend/`:

```env
OPENAI_API_KEY=sua_chave_aqui
```

### Rodar o backend

```bash
uvicorn main:app --reload
```

Backend disponível em:

```text
http://127.0.0.1:8000
```

Documentação da API:

```text
http://127.0.0.1:8000/docs
```

### Rodar o frontend

Em outro terminal:

```bash
cd frontend
python -m http.server 5500
```

Frontend disponível em:

```text
http://127.0.0.1:5500
```

---

## Variáveis de ambiente

```env
OPENAI_API_KEY=...
```

---

## Autor

**Bryan Duarte de Araujo Pereira**  
Estudante de Engenharia de Software focado em desenvolvimento, aprendizado contínuo e projetos práticos.
