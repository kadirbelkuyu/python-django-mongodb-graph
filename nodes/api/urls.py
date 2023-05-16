from django.urls import path
from rest_framework_mongoengine.routers import DefaultRouter
from .views import NodeViewSet, graph


router = DefaultRouter()
router.register(r'', NodeViewSet)

urlpatterns = [
    path('graph/', graph, name='graph'),
    path('graph/<str:node_id>/', graph, name='graph_with_id')
] + router.urls
