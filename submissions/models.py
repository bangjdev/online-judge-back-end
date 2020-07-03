from enum import Enum

from django.db import models
from django.contrib.auth.models import User

from lqdoj_backend.settings import SOURCE_CODE_FOLDER
from problems.models import Problem


class Language(models.Model):
    language = models.CharField(max_length=8, unique=True)
    compiler = models.CharField(max_length=256)
    source_extension = models.CharField(max_length=8, default="")

    def __str__(self):
        return self.language


class SubmissionStatus(object):
    PENDING = "PENDING_STATUS"
    COMPILING = "COMPILING_STATUS"
    JUDGING = "JUDGING_STATUS"
    COMPILE_ERROR = "COMPILE_ERROR_STATUS"
    FINISHED = "FINISHED_STATUS"


class Submission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, to_field="problem_code")
    source_code = models.TextField()
    language = models.ForeignKey(Language, models.CASCADE, to_field="language")
    status = models.CharField(max_length=100, default=SubmissionStatus.PENDING)
    test_counts = models.IntegerField(default=0)
    result = models.CharField(max_length=256, default="")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.__str__() + " submitted at " + self.time.__str__() + " using " + self.language.__str__()
