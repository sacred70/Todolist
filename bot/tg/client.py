import logging

import requests
from django.conf import settings
from pydantic import ValidationError

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse

logger = logging.getLogger(__name__)


class TgClient:
    def __init__(self, token: str = settings.BOT_TOKEN):
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(method='getUpdates', offset=offset, timeout=timeout)
        try:
            return GetUpdatesResponse(**data)
        except ValidationError as e:
            logger.error(str(e))
            logger.info(data)
            return GetUpdatesResponse(ok=False, result=[])

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get(method='sendMessage', chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def _get(self, method: str, **params) -> dict:
        url: str = self.get_url(method)
        response = requests.get(url, params=params)
        if not response.ok:
            logger.error(f'Status code: {response.status_code}. Body: {response.content}')
            raise RuntimeError
        return response.json()

"""import logging

from django.conf import settings
import requests
from pydantic.error_wrappers import ValidationError

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


logger = logging.getLogger(__name__)


class TgClientError(Exception):
    ...


class TgClient:
    def __init__(self, token: str | None = None):
        self.__token = token if token else settings.BOT_TOKEN
        self.__url = f'https://api.telegram.org/bot{self.__token}/'

    def __get_url(self, method: str) -> str:
        return f'{self.__url}{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60, **kwargs) -> GetUpdatesResponse:
        data = self._get('getUpdates', offset=offset, timeout=timeout, **kwargs)
        return self.__serialize_tg_response(GetUpdatesResponse, data)

    def send_message(self, chat_id: int, text: str, **kwargs) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id , text=text, **kwargs)
        return self.__serialize_tg_response(SendMessageResponse, data)

    def _get(self, method: str, **params) -> dict:
        url = self.__get_url(method)
        params.setdefault('timeout', 60)
        resource = requests.get(url, params=params)
        if not resource.ok:
            logger.warning('Invalid status code %d from command', resource.status_code, method)
            raise TgClientError
        return resource.json()

    @staticmethod
    def __serialize_tg_response(serialize_class, data: dict):
        try:
            return serialize_class(**data)
        except ValidationError:
            logger.error('Failed serialize telegram response: %s', data)
            raise TgClientError
#"""