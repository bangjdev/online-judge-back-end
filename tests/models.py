import hashlib
import os
import uuid

from django.db import models

from lqdoj_backend.settings import TEST_FOLDER
from problems.models import Problem


def get_encrypted_file_path(instance, filename):
    upload_to = os.path.join(hashlib.sha1(TEST_FOLDER.encode('UTF-8')).hexdigest())
    extension = os.path.splitext(filename)[1]
    filename = instance.problem.problem_code + uuid.uuid4().__str__()
    final_filename = '{}{}'.format(filename, extension)
    return os.path.join(upload_to, final_filename)


class Test(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, to_field="problem_code")
    name = models.CharField(max_length=50)
    position = models.IntegerField()
    input = models.FileField(upload_to=get_encrypted_file_path)
    output = models.FileField(upload_to=get_encrypted_file_path, )

