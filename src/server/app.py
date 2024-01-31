import datetime
import logging

import uvicorn
from fastapi import FastAPI, WebSocket

from api.model import MessageResponse, MessageResponseData, MicoMessage
from api.persona import HISTORY_TEACHER
from audio.asr import audio_to_text
from audio.vad import SpeechDetector
from common.constants import SESSION_TIMEOUT_SECONDS
from llm.copilot import GithubCopilot

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    _app = FastAPI()
    return _app


app = create_app()

# TODO support multiple sessions and prompts switching
gpt = GithubCopilot(prompt=HISTORY_TEACHER)
last_message_time: int = 0


# api for automatic speech recognition, accepts audio stream
@app.websocket("/ws/audio")
async def audio(websocket: WebSocket):
    await websocket.accept()

    sample_rate = 16000
    speech_detector = SpeechDetector(sample_rate=sample_rate)

    while True:
        data = await websocket.receive_bytes()
        if not speech_detector.process(data):
            text = audio_to_text(speech_detector.bytes_content)
            speech_detector.reset()
            await act(text)


@app.post("/message")
async def message(body: MicoMessage) -> MessageResponse:
    data = MessageResponseData(action="ignore")
    ignore_resp = MessageResponse(code=0, data=data)
    if not body.payload.is_final:
        return ignore_resp

    if body.payload.results is None:
        return ignore_resp

    text = body.payload.results[0].text
    if text is None:
        return ignore_resp
    if text in ["开灯", "关灯", "停", "大点声", "小点声", "几点了"]:
        return ignore_resp

    # TODO support multiple sessions
    global last_message_time
    now = datetime.datetime.now().timestamp()
    if now - last_message_time > SESSION_TIMEOUT_SECONDS:
        gpt.new_session()
    last_message_time = int(now)

    # TODO support new session trigger by user message
    logger.info(f"received text: {text}")
    text = gpt.chat(text) or ""
    logger.info(f"response text: {text}")
    return MessageResponse(code=0, data=MessageResponseData(action="tts", tts=text))


async def act(text: str) -> None:
    """
    do something with the text, e.g. send it to a chatbot
    :param text: text to process
    """
    logger.info(f"received text: {text}")
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
