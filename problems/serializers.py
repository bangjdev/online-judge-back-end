from rest_framework import serializers

from problems.models import Problem


class ProblemListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Problem
        fields = ('id', 'problem_code', 'title', 'difficulty', 'tags', )


class ProblemSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Problem
        fields = ('id', 'problem_code', 'title', 'author', 'tags', 'description', 'score_mode', 'last_modified', )
