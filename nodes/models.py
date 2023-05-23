from mongoengine import Document, StringField, ListField, DateTimeField, ReferenceField, BooleanField, IntField
from users.models import User


class PerformanceLabel(Document):
    label = StringField(max_length=100, null=True)
    value = IntField(null=True)
    user = ReferenceField(User, reverse_delete_rule=4, null=True)
    parent = ReferenceField('self', reverse_delete_rule=4, null=True)
    children = ListField(ReferenceField('self', reverse_delete_rule=4), null=True)

class Node(Document):
    BRANCH = 'Branş'
    TEAM = 'Takım'
    CATEGORY = 'Kategori'
    Kurum = 'Kurum'


    NODE_TYPE_CHOICES = [
        (BRANCH, 'Branş'),
        (TEAM, 'Takım'),
        (CATEGORY, 'Kategori'),
        (Kurum, 'Kurum'),
    ]

    name = StringField(max_length=100)
    teachers = ListField(ReferenceField(User, reverse_delete_rule=4))
    managers = ListField(ReferenceField(User, reverse_delete_rule=4))
    students = ListField(ReferenceField(User, reverse_delete_rule=4))
    # student_performance_labels = ListField(StringField())
    student_performance_labels = ListField(ReferenceField(PerformanceLabel, reverse_delete_rule=4), null=True)
    type = StringField(choices=NODE_TYPE_CHOICES, max_length=10)
    parent = ReferenceField('self', reverse_delete_rule=4, null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    children = ListField(ReferenceField('self', reverse_delete_rule=4))
    isactive = BooleanField(default=True)







#
# # Create your models here.
#
# class Node(Document):
#     BRANCH = 'Branş'
#     TEAM = 'Takım'
#     CATEGORY = 'Kategori'
#
#     NODE_TYPE_CHOICES = [
#         (BRANCH, 'Branş'),
#         (TEAM, 'Takım'),
#         (CATEGORY, 'Kategori'),
#     ]
#
#     name = StringField(max_length=100,)
#     teachers = ListField(ReferenceField(User, reverse_delete_rule=4), null=True, blank=True)
#     managers = ListField(ReferenceField(User, reverse_delete_rule=4), null=True, blank=True)
#     students = ListField(ReferenceField(User, reverse_delete_rule=4), null=True, blank=True)
#     student_performance_labels = ListField(StringField(), null=True)
#     type = StringField(choices=NODE_TYPE_CHOICES, max_length=10)
#     parent = ReferenceField('self', reverse_delete_rule=4, null=True)
#     created_at = DateTimeField(default=datetime.datetime.now, blank=True)
#     updated_at = DateTimeField(default=datetime.datetime.now, blank=True)
#     children = ListField(ReferenceField('self'), reverse_delete_rule=4, blank=True, null=True)
#
#     def save(self, *args, **kwargs):
#         if self.pk:
#             original = Node.objects.get(pk=self.pk)
#             if original.parent and original.parent != self.parent:
#                 original.parent.update(pull__children=original)
#
#         super().save(*args, **kwargs)
#
#         if self.parent:
#             self.parent.update(add_to_set__children=self)
#
#     def delete(self, *args, **kwargs):
#         if self.parent:
#             self.parent.update(pull__children=self)
#
#         super().delete(*args, **kwargs)
#     def update (self, *args, **kwargs):
#         self.updated_at = datetime.datetime.now()
#         super().update(*args, **kwargs)
