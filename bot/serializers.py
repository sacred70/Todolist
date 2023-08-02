from rest_framework import serializers


class VerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=16)


"""from rest_framework import serializers

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='chat_id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'username', 'verification_code', 'user_id')
        read_only_fields = ('tg_id', 'username', 'user_id')
        extra_kwargs = {'verification_code': {'write_only': True}}
"""