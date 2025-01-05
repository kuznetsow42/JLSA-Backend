from django.contrib import admin
from .models import Card, Tag, DictEntry


admin.site.register(Tag)
admin.site.register(DictEntry)

@admin.register(Card)
class CardsAdmin(admin.ModelAdmin):
    readonly_fields = ["dict_entry", "user"]
    list_select_related = True

