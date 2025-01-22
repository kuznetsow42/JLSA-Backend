from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Card, Tag
from .serializers import CardSerializer, TagSerializer


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created', 'visited', 'streak']
    filterset_fields = ["tags", "streak", ]

    def get_queryset(self):
        return self.request.user.cards.select_related("dict_entry").prefetch_related("tags", "dict_entry__kanji")
    

class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.tags.all()

    @action(detail=True, methods=["delete"])
    def delete_cards(self, request, pk):
        tag = self.get_queryset().prefetch_related("cards").get(id=pk)
        tag.cards.all().delete()
        tag.delete()
        return Response(status=204)

