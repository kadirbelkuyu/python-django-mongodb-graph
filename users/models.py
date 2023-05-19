from django.db.models.functions import datetime
from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, ReferenceField, IntField


class User(Document):
    first_name = StringField(max_length=100)
    last_name = StringField(max_length=100)
    tcNumber = StringField(max_length=11)
    phone = StringField(max_length=11)
    dateofBirth = DateTimeField()
    placeofBirth = StringField(max_length=100)
    contractStart = DateTimeField(auto_now_add=True)
    contractEnd = DateTimeField(auto_now=True)
    nationality = StringField(max_length=50)
    adress = StringField(max_length=100)
    otherAddress = StringField(max_length=100)
    isActive = BooleanField(default=True)
    permission = StringField(max_length=100)
    createdDate = DateTimeField(default=datetime.datetime.now, blank=True)
    modifiedDate = DateTimeField(default=datetime.datetime.now, blank=True)
    super_admin = BooleanField(default=False)

