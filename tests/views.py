# Create your views here.
from rest_framework import serializers

from submissions.models import Submission


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"
