from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot.models import TgUser
from bot.serializers import VerificationSerializer
from bot.tg.client import TgClient
from todolist.settings import TG_TOKEN


class VerificationView(APIView):
    serializer_class = VerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data.get('verification_code')

            tg_user = TgUser.objects.filter(verification_code=verification_code).first()
            if tg_user:
                tg_user.user_id = request.user.id
                tg_user.save()

                response_data = {
                    'tg_id': tg_user.tg_id,
                    'username': tg_user.username,
                    'verification_code': tg_user.verification_code,
                    'user_id': tg_user.user_id,
                }

                client = TgClient(TG_TOKEN)
                client.send_message(chat_id=tg_user.tg_id, text='You are successfully verified!')

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response('Telegram user not found', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""from typing import Any

from rest_framework import generics, permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationCodeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tg_user = TgUser.objects.get(verification_code=serializer.validated_data['verification_code'])
        except TgUser.DoesNotExist:
            raise AuthenticationFailed

        tg_user.user = request.user
        tg_user.save()
        TgClient().send_message(chat_id=tg_user.chat_id, text='Bot has been verified')
        return Response(TgUserSerializer(tg_user).data)
    """