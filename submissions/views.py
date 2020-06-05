# Create your views here.
from django.contrib.auth.models import User
from rest_framework import mixins, serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet

from lqdoj_backend.json_response import *
from lqdoj_backend.paginations import CustomPagination
from submissions.models import Submission, Language
from problems.models import Problem
from .tasks import run_judger


class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = "__all__"


class SubmissionsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Submission.objects.all()
    paginator = CustomPagination(page_size=10, page_size_query_param="limit", page_query_param="p")
    serializer_class = SubmissionsSerializer

    """
    Override POST method handler to create an async task queue
    """
    def create(self, request, *args, **kwargs):
        print("Receive a submission")
        submission_data = json.loads(request.body)
        print(submission_data)
        language = Language.objects.all().get(language=submission_data['language'])
        source_code = submission_data['source_code']
        author = User.objects.all().get(username=submission_data['author'])
        task = Problem.objects.all().get(task_code=submission_data['task'])
        new_submission = Submission(language=language, author=author, source_code=source_code, task=task)
        print(new_submission)
        new_submission.save()
        run_judger.delay(new_submission.id)
        return Response(data=create_message("SUBMITTED_SUCCESSFULLY"), status=HTTP_201_CREATED)