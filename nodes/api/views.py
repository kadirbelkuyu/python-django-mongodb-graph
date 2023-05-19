from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import NodeSerializer
from ..models import Node
from django.core.serializers import serialize
from django.http import JsonResponse

class NodeViewSet(ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

def get_children(node):
    children = Node.objects.filter(parent=node.id)
    children_data = []

    for child in children:
        child_data = {
            "id": str(child.id),
            "name": child.name,
            "type": child.type,
            "children": get_children(child)
        }
        children_data.append(child_data)

    return children_data

def graph(request, node_id=None):
    if node_id:
        root_node = Node.objects.get(id=node_id)
    else:
        root_node = Node.objects.filter(parent=None).first()

    if not root_node:
        return JsonResponse({"error": "Root node not found."}, status=404)

    graph_data = {
        "id": str(root_node.id),
        "name": root_node.name,
        "type": root_node.type,
        "children": get_children(root_node)
    }

    return JsonResponse(graph_data)