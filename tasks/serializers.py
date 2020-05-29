from rest_framework import serializers

from tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Task  
        fields = ('id', 'task_code', 'title', 'difficulty', 'tags', )


class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'task_code', 'title', 'author', 'tags', 'description', 'score_mode', 'last_modified', )
