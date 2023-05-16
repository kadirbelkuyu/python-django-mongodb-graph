from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import UserSerializer
from ..models import User

class UserViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailViewSet(ModelViewSet):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer