from collections import defaultdict
import io
import random
from django.core.files.images import ImageFile
import tempfile
from ebooklib import epub
from html.parser import HTMLParser
from fugashi import Tagger
import ebooklib
import re
from cards.models import DictEntry, Card, Deck, SubDeck, DeckCardRelation


class CustomParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ""
    

    def handle_data(self, data):
        self.text += re.sub(r'\s+', ' ', data)

    def get_text(self):
        text = self.text
        self.text = ""
        self.data = ""
        return text


def parse_epub(file):
    parser = CustomParser()
    chapters = []

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.flush()  
        book = epub.read_epub(temp_file.name)
        title_item = book.get_metadata("DC", "title")
        parser.feed(title_item[0][0])
        title = parser.get_text()
        cover_generator = book.get_items_of_type(ebooklib.ITEM_COVER)
        cover_bytes = next(cover_generator).get_content()
        cover = ImageFile(io.BytesIO(cover_bytes), name=f"{title}.jpg")
        for content in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            if content.is_chapter():
                parser.feed(content.get_body_content().decode())
                chapters.append(parser.get_text())

    return title, cover, chapters


def tokenize_text(chapters):
    tagger = Tagger()
    tokenized_chapters = {}
    for index, chapter in enumerate(chapters):
        tokens_dict = defaultdict(lambda: {"frequency": 0, "examples": []})
        sentences = chapter.split("。")
        if len(sentences) < 2:
            continue
        for sentence in sentences:
            tokens = tagger(sentence)
            for token in tokens:
                tokens_dict[token.surface]["frequency"] += 1
                tokens_dict[token.surface]["examples"].append(sentence)
        tokenized_chapters[f"Part {index}"] = tokens_dict
    return tokenized_chapters


def create_cards(file, user):
    title, cover, chapters = parse_epub(file)
    chapters_dict = tokenize_text(chapters)
    deck = Deck.objects.create(user=user, name=title, cover=cover)
    for chapter, words in chapters_dict.items():
        sub_deck = SubDeck.objects.create(name=chapter, parent=deck)
        dict_entries = DictEntry.objects.filter(word__in=words.keys())
        relations = []
        for entry in dict_entries:
            card = Card.objects.get_or_create(user=user, dict_entry=entry)[0]
            examples = random.choices(words[entry.word]["examples"], k=5)
            frequency = words[entry.word]["frequency"]
            relations.append(DeckCardRelation(card=card, deck=sub_deck, frequency=frequency, examples=examples))
        DeckCardRelation.objects.bulk_create(relations)

