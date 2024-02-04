from typing import List, Optional

from pydantic import BaseModel


class MicoMsgHeader(BaseModel):
    id: str
    name: str
    namespace: str
    dialog_id: str


class MicoMsgPayloadResult(BaseModel):
    confidence: Optional[float] = None
    text: Optional[str] = None
    asr_binary_offset: Optional[int] = None
    begin_offset: Optional[int] = None
    end_offset: Optional[int] = None
    behavior: Optional[str] = None


class MicoMsgPayload(BaseModel):
    is_final: Optional[bool] = None
    text: Optional[str] = None  # mi server response
    results: Optional[List[MicoMsgPayloadResult]] = None


class MicoMessage(BaseModel):
    header: MicoMsgHeader
    payload: MicoMsgPayload


class MessageResponseData(BaseModel):
    action: str
    tts: Optional[str] = None


class MessageResponse(BaseModel):
    code: int
    data: MessageResponseData
