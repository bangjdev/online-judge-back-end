# Create your views here.
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet

from lqdoj_backend.paginations import CustomPagination
from submissions.models import Submission
from tests.models import Test


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class TestsView(mixins.CreateModelMixin, GenericViewSet):
    queryset = Test.objects.all()
    paginator = CustomPagination(page_size=10, page_size_query_param="limit", page_query_param="p")
    serializer_class = TestsSerializer
