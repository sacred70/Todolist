from pydantic import BaseModel


class Chat(BaseModel):
    id: int


class Message(BaseModel):
    chat: Chat
    text: str | None = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message

"""from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    username: str | None = None


class Message(BaseModel):
    message_id: int
    chat: Chat
    text: str


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj] = []


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message
"""