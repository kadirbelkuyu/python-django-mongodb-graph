from rest_framework.relations import StringRelatedField
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from ..models import Node


# class ParrentSerializer(DocumentSerializer):
#     class Meta:
#         model = Node
#         fields = ('id', 'name', 'type')
#
# class RecursiveField(serializers.Serializer):
#     def to_representation(self, instance):
#         serializer = self.parent.parent.__class__(instance, context=self.context)
#         return serializer.data
#
# from rest_framework import serializers
# from rest_framework_mongoengine.serializers import DocumentSerializer
# from ..models import Node
#
# class NodeSerializer(DocumentSerializer):
#     parent = serializers.StringRelatedField(allow_null=True)  # parent alanına StringRelatedField kullan.
#     children = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Node
#         fields = '__all__'
#         depth = 1
#
#     def get_children(self, instance):
#         children = Node.objects.filter(parent=instance.id)
#         return NodeSerializer(children, many=True).data

#v2
class ParentChildNodeSerializer(DocumentSerializer):
    class Meta:
        model = Node
        fields = ('id', 'name', 'type')

class NodeSerializer(DocumentSerializer):
    parent = serializers.StringRelatedField(allow_null=True)
    # children = serializers.SerializerMethodField()
    # children = StringRelatedField(many=True)
    children = ParentChildNodeSerializer(many=True, read_only=True)   
    depth = 1 
    # children = serializers.StringRelatedField(many=True)

    class Meta:
        model = Node
        fields = '__all__'
        depth = 1

    def get_children(self, instance):
        children = Node.objects.filter(parent=instance.id)
        return NodeSerializer(children, many=True).data

# v3
# from rest_framework.relations import StringRelatedField
# from rest_framework_mongoengine.serializers import DocumentSerializer
# from rest_framework import serializers
# from ..models import Node


# class ChildrenSerializer(DocumentSerializer):
#     class Meta:
#         model = Node
#         fields = ('id', 'name', 'type')


# class NodeSerializer(DocumentSerializer):
#     parent = serializers.StringRelatedField(allow_null=True)
#     children = serializers.SerializerMethodField()

#     class Meta:
#         model = Node
#         fields = '__all__'
#         depth = 1

#     def get_children(self, instance):
#         children = Node.objects.filter(parent=instance.id)
#         return ChildrenSerializer(children, many=True).data

