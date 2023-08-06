from pydantic import BaseModel


class Chat(BaseModel):  # Представляет информацию о чате.
    id: int
    username: str | None = None


class Message(BaseModel):  # Представляет информацию о сообщении
    message_id: int
    chat: Chat
    text: str


class UpdateObj(BaseModel):  # Обертка для обновления, используется при получении обновлений через webhook.
    update_id: int
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):  # Представляет ответ на запрос метода getUpdates.
    ok: bool
    result: list[UpdateObj] = []


class SendMessageResponse(BaseModel):  # Представляет ответ на запрос метода sendMessage.
    ok: bool
    result: Message
