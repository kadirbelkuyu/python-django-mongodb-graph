from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from ..models import User

class UserSerializer(DocumentSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1