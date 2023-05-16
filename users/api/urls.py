from rest_framework_mongoengine.routers import DefaultRouter
from .views import UserViewSet, UserDetailViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', UserViewSet)


urlpatterns = router.urls