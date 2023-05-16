
from django.db import models
from django.db.models.functions import datetime
from mongoengine import Document, StringField, ListField, DateTimeField, ReferenceField, BooleanField
from users.models import User

# Create your models here.

class Node(Document):
    BRANCH = 'Branş'
    TEAM = 'Takım'
    CATEGORY = 'Kategori'

    NODE_TYPE_CHOICES = [
        (BRANCH, 'Branş'),
        (TEAM, 'Takım'),
        (CATEGORY, 'Kategori'),
    ]

    name = StringField(max_length=100,)
    teachers = ListField(ReferenceField(User, reverse_delete_rule=4), null=True, blank=True)
    managers = ListField(ReferenceField(User, reverse_delete_rule=4), null=True, blank=True)
    students = ListField(ReferenceField(User, reverse_delete_rule=4), null=True, blank=True)
    student_performance_labels = ListField(StringField(), null=True)
    type = StringField(choices=NODE_TYPE_CHOICES, max_length=10)
    parent = ReferenceField('self', reverse_delete_rule=4, null=True)
    created_at = DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = DateTimeField(default=datetime.datetime.now, blank=True)
    children = ListField(ReferenceField('self'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Node.objects.get(pk=self.pk)
            if original.parent and original.parent != self.parent:
                original.parent.update(pull__children=original)

        super().save(*args, **kwargs)

        if self.parent:
            self.parent.update(add_to_set__children=self)

    def delete(self, *args, **kwargs):
        if self.parent:
            self.parent.update(pull__children=self)

        super().delete(*args, **kwargs)
    def update (self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super().update(*args, **kwargs)