from rest_framework import serializers


class BookParserSerializer(serializers.Serializer):
    file = serializers.FileField()

