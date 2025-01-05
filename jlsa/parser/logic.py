import os
import tempfile
from ebooklib import epub
from html.parser import HTMLParser
from fugashi import Tagger
import ebooklib
import re
from cards.models import Card, DictEntry


class CustomParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = ""
    

    def handle_data(self, data):
        self.text += re.sub(r'\s+', ' ', data)


def parse_epub(file):
    parser = CustomParser()

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.flush()  
        book = epub.read_epub(temp_file.name)
        title = book.get_metadata('DC', 'title')

        for content in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            parser.feed(content.get_body_content().decode())
    tokenize_text(parser.text)

    return {"text": parser.text, "title": title}


def tokenize_text(text):
    tagger = Tagger()

    tokens = tagger(text)
    unique_tokens = set([token.feature.lemma for token in tokens])
    return unique_tokens


def create_cards(file, user):
    parsed_epub = parse_epub(file)
    words = tokenize_text(parsed_epub["text"])
    cards = []
    for word in words:
        dict_entry = DictEntry.objects.filter(word=word)
        if not dict_entry:
            continue
        card = Card.objects.get_or_create(dict_entry=dict_entry.first(), user=user)[0]
        card.tags.add(parsed_epub["title"])
        card.save()
        cards.append(card)
    return cards

