from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Card, Deck
from .serializers import DeckSerializer, CardSerializer, UpdateCardsSerializer


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['created', 'visited', 'streak']
    filterset_fields = ["streak", ]

    def get_queryset(self):
        return Card.objects.select_related("dict_entry", "user").prefetch_related("dict_entry__kanji").filter(user=self.request.user)
    
    @action(detail=False, methods=["patch", "delete"])
    def sync(self, request):
        serializer = UpdateCardsSerializer(data=request.data.get("cards"), partial=True, context={"queryset": self.get_queryset()})
        serializer.is_valid(raise_exception=True)
        if request.method == "DELETE":
            amount = serializer.bulk_delete()
            return Response(f"Deleted {amount} card(s)", status=204)
        cards = serializer.bulk_update()
        return Response(cards, status=200)
    

class DeckView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(user=self.request.user, parent=None).prefetch_related("cards", "sub_decks").all()


