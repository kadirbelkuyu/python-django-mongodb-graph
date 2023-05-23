from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from ..models import Node, PerformanceLabel

class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

class PerformanceLabelSerializer(DocumentSerializer):
    class Meta:
        model = PerformanceLabel
        fields = '__all__'
        depth = 1


class NodeSerializer(DocumentSerializer):
    student_performance_labels = PerformanceLabelSerializer(many=True, allow_null=True, read_only=True)
    parent = serializers.CharField(read_only=True, allow_null=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        depth = 1

    def update(self, instance, validated_data):
        parent_id = validated_data.pop('parent', None)
        if parent_id:
            parent = Node.objects.get(id=parent_id)
            instance.parent = parent
        return super().update(instance, validated_data)
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



"""
{
    "name": "Node Name",
    "teachers": ["teacher_id1", "teacher_id2"],
    "managers": ["manager_id1", "manager_id2"],
    "students": ["student_id1", "student_id2"],
    "student_performance_labels": [
        {
            "label": "Futbol",
            "user": "user_id",
            "value": 5,
            "children": [
                {
                    "label": "Sarı Kart",
                    "user": "user_id",
                    "value": 2
                },
                {
                    "label": "Kırmızı Kart",
                    "user": "user_id",
                    "value": 1
                }
            ]
        }
    ],
    "type": "Takım",
    "parent": "parent_node_id",
    "children": ["child_node_id1", "child_node_id2"],
    "isactive": true
}

"""