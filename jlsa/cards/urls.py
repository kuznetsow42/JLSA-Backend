from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CardViewSet, DeckView


router = SimpleRouter()
router.register("decks", DeckView, "decks")
router.register("", CardViewSet, "cards")

urlpatterns = router.urls

