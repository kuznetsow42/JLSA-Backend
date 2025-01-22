from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CardViewSet, TagViewSet


router = SimpleRouter()
router.register("tags", TagViewSet, "tags")
router.register("", CardViewSet, "cards")

urlpatterns = router.urls

