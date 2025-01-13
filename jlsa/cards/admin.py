from django.contrib import admin
from .models import Card, Tag, DictEntry, Kanji


admin.site.register(Tag)
admin.site.register(Kanji)

@admin.register(Card)
class CardsAdmin(admin.ModelAdmin):
    readonly_fields = ["dict_entry", "user"]
    list_select_related = True


@admin.register(DictEntry)
class DictEntryAdmin(admin.ModelAdmin):
    readonly_fields = ["kanji"]
    list_select_related = True

