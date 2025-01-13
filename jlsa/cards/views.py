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
    
    @action(detail=False)
    def get_tags(self, request):
        tags = self.request.user.tags.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

