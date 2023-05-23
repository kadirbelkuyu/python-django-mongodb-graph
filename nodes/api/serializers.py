from bson.errors import InvalidId
from mongomock.object_id import ObjectId
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
    parent = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all(), allow_null=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'children']
        depth = 1

    def to_representation(self, instance):
        self.fields['parent'] = NodeSerializer()
        self.fields['children'] = NodeSerializer(many=True)
        return super(NodeSerializer, self).to_representation(instance)

    def update(self, instance, validated_data):
        parent_id = validated_data.get('parent_id', None)
        performance_label_id = validated_data.get('performance_label_id', None)

        if parent_id is not None:
            try:
                ObjectId(parent_id)
            except InvalidId:
                raise serializers.ValidationError(
                    "Invalid parent_id. It must be a 12-byte input or a 24-character hex string.")

            try:
                parent = Node.objects.get(id=parent_id)
            except Node.DoesNotExist:
                raise serializers.ValidationError("No Node with that parent_id exists.")

            instance.parent = parent

        if performance_label_id is not None:
            try:
                ObjectId(performance_label_id)
            except InvalidId:
                raise serializers.ValidationError(
                    "Invalid performance_label_id. It must be a 12-byte input or a 24-character hex string.")

            try:
                performance_label = PerformanceLabel.objects.get(id=performance_label_id)
            except PerformanceLabel.DoesNotExist:
                raise serializers.ValidationError(
                    "No PerformanceLabel with that performance_label_id exists.")

            instance.student_performance_label = performance_label

        instance.save()
        return super().update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     parent_id = validated_data.get('parent_id', None)
    #
    #     if parent_id is not None:
    #         # Check if parent_id is a valid ObjectId
    #         try:
    #             ObjectId(parent_id)
    #         except InvalidId:
    #             raise serializers.ValidationError(
    #                 "Invalid parent_id. It must be a 12-byte input or a 24-character hex string.")
    #
    #         try:
    #             parent = Node.objects.get(id=parent_id)
    #         except Node.DoesNotExist:
    #             raise serializers.ValidationError("No Node with that parent_id exists.")
    #
    #         # Your update logic goes here
    #         # Ensure this logic returns the updated instance
    #         instance.parent = parent
    #         instance.save()
    #
    #     return super().update(instance, validated_data)

    def create(self, validated_data):
        parent_id = validated_data.pop('parent', None)
        if parent_id:
            parent = Node.objects.get(id=parent_id)
            instance = Node.objects.create(parent=parent, **validated_data)
        else:
            instance = Node.objects.create(**validated_data)
        return instance

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