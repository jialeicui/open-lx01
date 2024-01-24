import logging

import uvicorn
from fastapi import FastAPI, WebSocket

from api.model import MicoMessage
from audio.asr import audio_to_text
from audio.vad import SpeechDetector
from llm.copilot import GithubCopilot

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    _app = FastAPI()
    return _app


app = create_app()


# api for automatic speech recognition, accepts audio stream
@app.websocket("/ws/audio")
async def audio(websocket: WebSocket):
    await websocket.accept()

    sample_rate = 16000
    speech_detector = SpeechDetector(sample_rate=sample_rate)

    while True:
        data = await websocket.receive_bytes()
        if not speech_detector.process(data):
            text = audio_to_text(speech_detector.bytes)
            speech_detector.reset()
            await act(text)


@app.post("/message")
async def message(body: MicoMessage) -> None:
    if not body.payload.is_final:
        return

    text = body.payload.results[0].text
    logger.info(f"received text: {text}")
    gpt = GithubCopilot()
    text = gpt.chat(text)
    logger.info(f"response text: {text}")


async def act(text: str) -> None:
    """
    do something with the text, e.g. send it to a chatbot
    :param text: text to process
    """
    logger.info(f"received text: {text}")
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
