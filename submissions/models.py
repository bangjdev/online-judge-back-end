from enum import Enum
import os, hashlib, uuid

from django.db import models
from django.contrib.auth.models import User

from lqdoj_backend.settings import SOURCE_CODE_FOLDER
from problems.models import Problem


class Language(models.Model):
    language = models.CharField(max_length=8, unique=True)
    compiler = models.CharField(max_length=256)

    def __str__(self):
        return self.language


class SubmissionStatus(Enum):
    PENDING = "PENDING_STATUS"
    JUDGING = "JUDGING_STATUS"
    FINISHED = "FINISHED_STATUS"


def get_encrypted_file_path(instance, filename):
    upload_to = os.path.join(hashlib.sha1(SOURCE_CODE_FOLDER.encode('UTF-8')).hexdigest())
    extension = os.path.splitext(filename)[1]
    filename = instance.author.username + uuid.uuid4().__str__()
    final_filename = '{}{}'.format(filename, extension)
    return os.path.join(upload_to, final_filename)


class Submission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username")
    task = models.ForeignKey(Problem, on_delete=models.CASCADE, to_field="task_code")
    source_code = models.FileField(upload_to=get_encrypted_file_path)
    language = models.ForeignKey(Language, models.CASCADE, to_field="language")
    status = models.CharField(max_length=20, choices=[(status.name, status.value) for status in SubmissionStatus],
                              default=SubmissionStatus.PENDING)
    test_counts = models.IntegerField(default=0)
    result = models.CharField(max_length=256, default="")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.__str__() + " submitted at " + self.time.__str__() + " using " + self.language.__str__()
