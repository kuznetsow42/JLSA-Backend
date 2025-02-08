from django.contrib import admin
from .models import Deck, Card, DictEntry, Kanji


admin.site.register(Deck)
admin.site.register(Kanji)

@admin.register(Card)
class CardsAdmin(admin.ModelAdmin):
    raw_id_fields = ["dict_entry", "user"]
    list_select_related = True


@admin.register(DictEntry)
class DictEntryAdmin(admin.ModelAdmin):
    raw_id_fields = ["kanji"]
    list_select_related = True


