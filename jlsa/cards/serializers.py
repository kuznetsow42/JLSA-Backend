from rest_framework import serializers
from .models import Card, Tag


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        exclude = ["user"]
        depth = 2


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["user"]

