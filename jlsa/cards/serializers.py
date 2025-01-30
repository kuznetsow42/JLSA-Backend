from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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


class UpdateCardsSerializer(serializers.ListSerializer):
    child = CardSerializer()

    def run_child_validation(self, data):
        if "id" not in data:
            raise ValidationError({"id": "Missing id field."})
        if "visited" not in data:
            data["visited"] = datetime.now()
        return super().run_child_validation(data)


    def validate(self, attrs):     
        queryset = self.context.get("queryset")
        if queryset is None:
            raise TypeError("Queryset with user's cards is required")
        id_list = [data["id"] for data in self.initial_data]
        self.cards_to_update = queryset.filter(id__in=id_list)
        if len(self.cards_to_update) != len(id_list):
            raise ValidationError({"cards": f"Couldn't find cards with following ids: {', '.join([str(id) for id in id_list])}"})
        return attrs

    def bulk_update(self):
        result = []
        for card, data in zip(self.cards_to_update, self.validated_data):
            print(data)
            result.append(self.child.update(card, data))
        return self.to_representation(result)
    
    def bulk_delete(self):
        result = self.cards_to_update.delete()
        return result[0]

    