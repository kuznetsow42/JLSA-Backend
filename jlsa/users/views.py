from rest_framework.generics import CreateAPIView, ListAPIView
from .models import User
from .serializers import UserSerializer, UserListSerializer


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListUsers(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

