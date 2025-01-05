from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User


class DictEntry(models.Model):
    word = models.CharField(max_length=128)
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


class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Card(models.Model):
    dict_entry = models.ForeignKey(DictEntry, on_delete=models.CASCADE, related_name="cards")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    streak = models.PositiveSmallIntegerField(default=0)
    learned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    visited = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return f"{str(self.dict_entry)} | {str(self.user)}"

