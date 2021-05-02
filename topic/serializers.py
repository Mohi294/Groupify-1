from rest_framework import serializers
from topic.models import Topic
from rest_framework_recursive.fields import RecursiveField


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')


class TopicSubtreeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'children')
        read_only_fields = ('id', 'name', 'children')