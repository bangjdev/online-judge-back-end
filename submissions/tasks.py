from celery import shared_task

from submissions.models import Submission
from submissions.models import SubmissionStatus
from problems.models import Test


@shared_task
def update_submission_status(submission, current_test, result):
    if (not current_test) and result:  # Finished
        submission.status = SubmissionStatus.FINISHED
        submission.result = result
    else:
        if current_test and (not result):
            submission.status = SubmissionStatus.JUDGING
            submission.test_counts = current_test

    submission.save()


def load_tests(task_code):
    return Test.objects.all().get(task_code=task_code)

@shared_task
def run_judger(submission_id):
    submission = Submission.objects.all().get(id=submission_id)
    tests_set = load_tests(submission.task)
