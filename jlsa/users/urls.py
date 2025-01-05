from django.urls import path, include
from .views import CreateUser, ListUsers


urlpatterns = [
    path("auth/", include("durin.urls")),
    path("auth/register/", CreateUser.as_view()),
    path("", ListUsers.as_view()),
]

