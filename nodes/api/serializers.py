from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from ..models import Node


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class NodeSerializer(DocumentSerializer):
    parent = serializers.CharField(read_only=True, allow_null=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = '__all__'
        depth = 1

    def get_children(self, instance):
        children = Node.objects.filter(parent=instance.id)
        children_data = []

        for child in children:
            child_data = {
                "id": str(child.id),
                "name": child.name,
                "type": child.type,
                "children": self.get_children(child),
                "teachers": child.teachers,
                "managers": child.managers,
                "students": child.students,
                "student_performance_labels": child.student_performance_labels,
            }
            children_data.append(child_data)

        return children_data

    def create(self, validated_data):
        parent_id = self.context['request'].data.get('parent')
        if parent_id:
            parent = Node.objects.get(id=parent_id)
            instance = Node.objects.create(parent=parent, **validated_data)
            parent.children.append(instance)
            parent.save()
        else:
            instance = Node.objects.create(**validated_data)
        return instance
