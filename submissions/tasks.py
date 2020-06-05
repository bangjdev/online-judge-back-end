from time import sleep

from celery import shared_task

from submissions.models import Submission
from submissions.models import SubmissionStatus
from problems.models import Test


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
    submission = Submission.objects.all().get(id=submission_id)
    tests_set = load_tests(submission.task)
    for test in tests_set:
        sleep(5)
        update_submission_status(submission=submission, current_test=test.position)
    update_submission_status(submission=submission, result="ACCEPTED")