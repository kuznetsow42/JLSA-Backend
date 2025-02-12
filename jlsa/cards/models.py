from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User


class Kanji(models.Model):
    character = models.CharField(max_length=2)
    strokes = models.PositiveSmallIntegerField()
    meanings = ArrayField(models.TextField())
    kun = ArrayField(models.CharField(max_length=16), null=True, blank=True)
    on = ArrayField(models.CharField(max_length=16), null=True, blank=True)
    name_readings = ArrayField(models.CharField(max_length=16), null=True, blank=True)

    def __str__(self):
        return self.character
    
    class Meta:
         verbose_name_plural = "Kanji"
         indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["character"])
         ]


class DictEntry(models.Model):
    word = models.CharField(max_length=128)
    kanji = models.ManyToManyField(Kanji, related_name="words", blank=True)
    reading = models.CharField(max_length=128)
    definitions = ArrayField(models.TextField())

    def __str__(self):
        return self.word

    class Meta:
         verbose_name_plural = "Dict entries"
         indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["word"])
         ]


class Card(models.Model):
    dict_entry = models.ForeignKey(DictEntry, on_delete=models.CASCADE, related_name="cards")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    streak = models.PositiveSmallIntegerField(default=0)
    learned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    visited = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{str(self.dict_entry)} | {str(self.user)}"


class Deck(models.Model):
    cover = models.ImageField(upload_to="decks/", null=True, blank=True)
    name = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decks")
    
    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("user", "name")


class SubDeck(models.Model):
    parent = models.ForeignKey(Deck, on_delete=models.CASCADE, blank=True, null=True, related_name="sub_decks")
    name = models.CharField(max_length=128)
    cards = models.ManyToManyField(Card, through="DeckCardRelation")

    def __str__(self):
        return f"{self.name} | {self.parent}"

class DeckCardRelation(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="deck_relations")
    deck = models.ForeignKey(SubDeck, on_delete=models.CASCADE, related_name="card_relations")
    frequency = models.PositiveIntegerField()
    examples = ArrayField(models.TextField())

    def __str__(self):
        return f"{self.deck} | {self.card.dict_entry}"

