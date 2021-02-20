""" models.py """

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField,
    DateTimeField
)


class Article(Document):
    meta = {"collection": "Scraping_collection_predicted"}

    text = StringField()
    date = DateTimeField()
    prediction = StringField()
