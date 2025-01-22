from rest_framework import serializers
from .models import Card, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ["user"]


class CardSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Card
        exclude = ["user"]
        depth = 2

