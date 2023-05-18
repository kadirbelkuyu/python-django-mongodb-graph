from django.db import models
from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, ReferenceField
# Create your models here.


class Injury(Document):
    name = StringField(max_length=100)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    isactive = BooleanField(default=True)


class InfoInjury(Document):
    name = StringField(max_length=100)
    description = StringField(max_length=100)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    isactive = BooleanField(default=True)
    status = BooleanField(default=True)