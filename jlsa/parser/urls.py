from django.urls import path
from .views import ParseBook


urlpatterns = [
    path("parse_book/", ParseBook.as_view())
]

