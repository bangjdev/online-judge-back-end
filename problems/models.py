from django.contrib.auth.models import User
from django.db import models
from enum import Enum


class ScoreModeEnum(Enum):
    SUM = "SUM"
    GROUP_MIN = "GROUP_MIN"


class DifficultyEnum(Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class DiffModeEnum(Enum):
    C1 = "C1"


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.tag_name


class Problem(models.Model):
    task_code = models.CharField(max_length=16, unique=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, to_field="username")
    difficulty = models.CharField(max_length=20, choices=[(diff.name, diff.value) for diff in DifficultyEnum])
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    score_mode = models.CharField(max_length=20, choices=[(mode.name, mode.value) for mode in ScoreModeEnum])
    score_parameter = models.TextField()
    time_limit = models.FloatField(default=1)
    memory_limit = models.IntegerField(default=256)
    diff_mode = models.CharField(max_length=20, choices=[(mode.name, mode.value) for mode in DiffModeEnum])
    custom_grader = models.FileField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def problem_tags(self):
        return "; ".join([p.tag_name for p in self.tags.all()])

    def __str__(self):
        return self.task_code + " by " + self.author.__str__()


class Test(models.Model):
    task = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    position = models.IntegerField()
    input = models.FileField()
    output = models.FileField()

