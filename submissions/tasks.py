from time import sleep
import os, hashlib, uuid, subprocess

from celery import shared_task

from online_judger_backend.settings import BASE_DIR, MEDIA_ROOT, JUDGER_ERRORS
from submissions.models import Submission, Language
from submissions.models import SubmissionStatus
from tests.models import Test
from online_judger_backend.settings import SOURCE_CODE_FOLDER

OUTPUT_EXEC_PATH = os.path.join(BASE_DIR, os.path.join(MEDIA_ROOT, "tmp"))
OUTPUT_EXEC_NAME = "userexec"
JUDGER_COMMAND_FMT = "judger/judger -c {} -if {} -of {} -ck {} -uo {} -m {} -t {}"


def update_submission_status(submission, status=None, result=None, current_test=None):
    if result:
        submission.result = result
        submission.status = SubmissionStatus.FINISHED
    if status:
        submission.status = status
    if current_test:
        submission.test_counts = current_test
    submission.save()


def load_tests(problem_code):
    return Test.objects.all().filter(problem=problem_code).order_by("position")


def write_to_encrypted_file_path(author, content, extension):
    upload_to = os.path.join(MEDIA_ROOT, hashlib.sha1(SOURCE_CODE_FOLDER.encode('UTF-8')).hexdigest())
    filename = author.username + "_" + uuid.uuid4().__str__()
    final_filename = '{}.{}'.format(filename, extension)

    final_filepath = os.path.join(upload_to, final_filename)

    file_writer = open(final_filepath, "w")
    file_writer.write(content)
    file_writer.close()

    return final_filepath


@shared_task
def run_judger(submission_id):
    # Get the submission data
    submission = Submission.objects.all().get(id=submission_id)
    source_code_file = write_to_encrypted_file_path(submission.author, submission.source_code, submission.language.source_extension)

    # Run compiler
    code_exec_name = submission.author.username + "_" + uuid.uuid4().__str__() + "_" + OUTPUT_EXEC_NAME
    output_exec_path = os.path.join(OUTPUT_EXEC_PATH, code_exec_name)

    update_submission_status(submission=submission, status=SubmissionStatus.COMPILING)
    compiler = Language.objects.get(language=submission.language).compiler
    compile_code = subprocess.call(compiler.format(output_exec_path, source_code_file), shell=True)

    if compile_code != 0:
        update_submission_status(
            submission, status=SubmissionStatus.FINISHED, result=SubmissionStatus.COMPILE_ERROR)
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
        user_output_file = code_exec_name + ".out"
        mem_lim = test.problem.memory_limit
        time_lim = test.problem.time_limit
        judge_code = subprocess.call(JUDGER_COMMAND_FMT.format(
            output_exec_path,
            test_input_file,
            test_output_file,
            checker,
            user_output_file,
            mem_lim,
            time_lim
        ), shell=True)
        print(JUDGER_COMMAND_FMT.format(
            output_exec_path,
            test_input_file,
            test_output_file,
            checker,
            user_output_file,
            mem_lim,
            time_lim
        ))
        print("Judger returned ", judge_code)
        if judge_code != 0:
            update_submission_status(
                submission=submission, status=SubmissionStatus.FINISHED, result=JUDGER_ERRORS[judge_code])
            return JUDGER_ERRORS[judge_code]
        else:
            update_submission_status(submission=submission, status=SubmissionStatus.JUDGING, current_test=test.position)
        # sleep(5) # pseudo time lag
    update_submission_status(submission=submission, status=SubmissionStatus.FINISHED, result=JUDGER_ERRORS[0])

    # Clean up
    # subprocess.call("rm -f " + source_code_file, shell=True)
    # subprocess.call("rm -f " + output_exec_path, shell=True)

    return JUDGER_ERRORS[0]
