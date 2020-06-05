import os
from time import sleep

from celery import shared_task

from lqdoj_backend.settings import BASE_DIR, MEDIA_ROOT, JUDGER_ERRORS
from submissions.models import Submission, Language
from submissions.models import SubmissionStatus
from tests.models import Test

OUTPUT_EXEC_PATH = os.path.join(BASE_DIR, os.path.join(MEDIA_ROOT, "tmp"))
OUTPUT_EXEC_NAME = "userexec"
JUDGER_COMMAND_FMT = "judger/judger -c {} -if {} -of {} -ck {} -uo {} -m {} -t {}"


def update_submission_status(submission, status=None, current_test=None, result=None):
    if status:
        submission.status = status
    if (not current_test) and result:  # Finished
        submission.status = SubmissionStatus.FINISHED
        submission.result = result
    else:
        if current_test and (not result):
            submission.status = SubmissionStatus.JUDGING
            submission.test_counts = current_test

    submission.save()


def load_tests(problem_code):
    return Test.objects.all().filter(problem=problem_code).order_by("position")


@shared_task
def run_judger(submission_id):
    # Get the submission data
    submission = Submission.objects.all().get(id=submission_id)

    # Run compiler
    update_submission_status(submission, status=SubmissionStatus.COMPILING)
    output_exec_path = os.path.join(OUTPUT_EXEC_PATH, OUTPUT_EXEC_NAME)
    compiler = Language.objects.get(language=submission.language).compiler
    compile_code = os.system(compiler.format(output_exec_path, submission.source_code.path))
    if compile_code != 0:
        update_submission_status(submission, status=SubmissionStatus.FINISHED, result="COMPILE_ERROR")
        return "COMPILE_ERROR"

    # Get set of tests
    tests_set = load_tests(submission.problem)
    # Judging using judger
    update_submission_status(submission, status=SubmissionStatus.JUDGING)
    for test in tests_set:
        test_input_file = test.input.path
        test_output_file = test.output.path
        checker = test.problem.custom_grader
        if not checker:
            checker = "diff"
        user_output_file = OUTPUT_EXEC_NAME + ".out"
        mem_lim = test.problem.memory_limit
        time_lim = test.problem.time_limit
        judge_code = os.system(JUDGER_COMMAND_FMT.format(
            output_exec_path,
            test_input_file,
            test_output_file,
            checker,
            user_output_file,
            mem_lim,
            time_lim
        ))
        if judge_code != 0:
            update_submission_status(submission, status=SubmissionStatus.FINISHED, result=JUDGER_ERRORS[judge_code])
            return JUDGER_ERRORS[judge_code]
        else:
            update_submission_status(submission, current_test=test.position)
        sleep(5) # pseudo time lag
    update_submission_status(submission, status=SubmissionStatus.FINISHED, result=JUDGER_ERRORS[0])
    return JUDGER_ERRORS[0]
