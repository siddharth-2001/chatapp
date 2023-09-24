from rest_framework import serializers


class CreateChatSerializer(serializers.Serializer):
    recipient = serializers.IntegerField()