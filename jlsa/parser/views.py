from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import BookParserSerializer
from .logic import create_cards


class ParseBook(APIView):
    serializer_class = BookParserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookParserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            file = serializer.validated_data["file"]
            cards = create_cards(file, user)
        return Response(data=cards, status=201)

