# Create your views here.
from django import forms
from rest_framework import mixins, serializers, permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.viewsets import GenericViewSet

from lqdoj_backend.json_response import *
from lqdoj_backend.paginations import CustomPagination
from submissions.models import Submission
from submissions.tasks import run_judger


class SubmissionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("id", "author", "problem", "language", "result", "time", )

class SubmissionDetailSerializer(serializers.ModelSerializer):
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

    """
    Override POST method handler to create an async problem queue
    """
    def create(self, request, *args, **kwargs):
        print("Receive a submission")
        print(json.loads(request.body))

        author = request.auth

        if author is None:
            return Response(data=create_message("SUBMITTED_FAIL", results={"author": "NEED_LOGIN"}), status=HTTP_403_FORBIDDEN)

        submission_data = json.loads(request.body)
        submission_data['author'] = author.user.username

        submission_form = SubmissionForm(data=submission_data)

        if submission_form.is_valid():
            new_submission = submission_form.save()
            run_judger.delay(new_submission.id)
            return Response(data=create_message("SUBMITTED_SUCCESSFULLY"), status=HTTP_201_CREATED)
        else:
            return Response(data=create_message("SUBMITTED_FAIL", results=submission_form.errors), status=HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, *args, **kwargs):
        if request.auth is None:
            return Response(data=create_message(
                                    message_code="LOADED_FAIL", 
                                    results={}), 
                            status=HTTP_403_FORBIDDEN)
        submission = self.get_queryset().get(id=kwargs['pk'])
        serialized_submission = SubmissionDetailSerializer(submission).data
        return Response(data=create_message(
                                message_code="LOADED_SUCCESSFULLY", 
                                results=serialized_submission), 
                        status=HTTP_200_OK)

    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubmissionDetailSerializer
        else:
            return SubmissionsListSerializer
