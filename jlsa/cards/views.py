from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Card, Tag
from .serializers import CardSerializer, TagSerializer, UpdateCardsSerializer


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created', 'visited', 'streak']
    filterset_fields = ["tags", "streak", ]

    def get_queryset(self):
        return Card.objects.select_related("dict_entry", "user").prefetch_related("tags", "dict_entry__kanji").filter(user=self.request.user)
    
    @action(detail=False, methods=["patch", "delete"])
    def sync(self, request):
        serializer = UpdateCardsSerializer(data=request.data.get("cards"), partial=True, context={"queryset": self.get_queryset()})
        serializer.is_valid(raise_exception=True)
        if request.method == "DELETE":
            amount = serializer.bulk_delete()
            return Response(f"Deleted {amount} card(s)", status=204)
        cards = serializer.bulk_update()
        return Response(cards, status=200)
    

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

