from time import sleep
import os

from celery import shared_task

from submissions.models import Submission, Language
from submissions.models import SubmissionStatus
from problems.models import Test


OUTPUT_EXEC_NAME = "userexec"

def update_submission_status(submission, current_test=None, result=None):
    if (not current_test) and result:  # Finished
        submission.status = SubmissionStatus.FINISHED
        submission.result = result
    else:
        if current_test and (not result):
            submission.status = SubmissionStatus.JUDGING
            submission.test_counts = current_test

    submission.save()


def load_tests(task_code):
    return Test.objects.all().filter(task=task_code)


@shared_task
def run_judger(submission_id):
    # Get the submission data
    submission = Submission.objects.all().get(id=submission_id)
    # Get compiler info
    compiler = Language.objects.get(language=submission.language)
    compile_code = os.system(compiler + OUTPUT_EXEC_NAME + " " + submission.source_code)
    tests_set = load_tests(submission.task)
    return tests_set.first().input.path
    # for test in tests_set:
    #     sleep(5)
    #     update_submission_status(submission=submission, current_test=test.position)
    # update_submission_status(submission=submission, result="ACCEPTED")