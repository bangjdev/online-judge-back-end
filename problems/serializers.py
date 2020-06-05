from rest_framework import serializers

from problems.models import Problem


class TaskListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Problem
        fields = ('id', 'task_code', 'title', 'difficulty', 'tags', )


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Problem
        fields = ('id', 'task_code', 'title', 'author', 'tags', 'description', 'score_mode', 'last_modified', )
