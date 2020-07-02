# Create your views here.
from django import forms
from rest_framework import mixins, serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from lqdoj_backend.json_response import *
from lqdoj_backend.paginations import CustomPagination
from submissions.models import Submission
from submissions.tasks import run_judger


class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("language", "source_code", "author", "problem",)


class SubmissionsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Submission.objects.all().order_by("-time")
    paginator = CustomPagination(page_size=10, page_size_query_param="limit", page_query_param="p")
    serializer_class = SubmissionsSerializer

    """
    Override POST method handler to create an async problem queue
    """
    def create(self, request, *args, **kwargs):
        print("Receive a submission")

        submission_data = request.data.dict()

        submission_form = SubmissionForm(data=request.data.dict())

        if submission_form.is_valid():
            new_submission = submission_form.save()
            run_judger.delay(new_submission.id)
            return Response(data=create_message("SUBMITTED_SUCCESSFULLY"), status=HTTP_201_CREATED)
        else:
            return Response(data=create_message("SUBMITTED_FAIL", results=submission_form.errors), status=HTTP_400_BAD_REQUEST)
