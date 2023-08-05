from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
import json
import inspect
import importlib
import time
from smoketest import SmokeTest, ApplicationTestResultSet


def test_class(cls):
    o = cls()
    return o.run()


def test_application(app):
    """ should return an ApplicationTestResultSet """
    num_test_classes = 0
    num_tests_run = 0
    num_tests_passed = 0
    num_tests_failed = 0
    num_tests_errored = 0

    failed_tests = []
    errored_tests = []

    a = None
    try:
        a = importlib.import_module("%s.smoke" % app)
    except ImportError:
        # no 'smokes' module for the app
        pass
    except Exception, e:
        num_tests_errored += 1
        errored_tests.append(
            'Exception while importing smoke test script: %s' % e)

    if a is not None:
        e_tests = []
        try:
            for name, obj in inspect.getmembers(a, inspect.isclass):
                if not issubclass(obj, SmokeTest):
                    continue
                if name == "SmokeTest":
                    # skip the parent class, which is usually imported
                    continue
                num_test_classes += 1
                (run, passed, failed, errored,
                 f_tests, e_tests) = test_class(obj)
                num_tests_run += run
                num_tests_passed += passed
                num_tests_failed += failed
                num_tests_errored += errored
                failed_tests = failed_tests + f_tests
                errored_tests = errored_tests + e_tests
        except Exception, e:
            # probably an error in setUp() or tearDown()
            num_tests_errored += 1
            e_tests.append('Exception during test: %s' % e)
        finally:
            errored_tests = errored_tests + e_tests
    return ApplicationTestResultSet(
        num_test_classes, num_tests_run,
        num_tests_passed, num_tests_errored,
        num_tests_failed, failed_tests,
        errored_tests)


def make_failed_report(result_sets):
    return "\n\n".join(
        [f for f in reduce(
            lambda x, y: x + y, [r.failed for r in result_sets])])


def make_errored_report(result_sets):
    return "\n\n".join(
        [f for f in reduce(
            lambda x, y: x + y, [r.errored for r in result_sets])])


def plaintext_output(status, num_test_classes, num_tests_run,
                     num_tests_passed, num_tests_failed,
                     num_tests_errored, finish, start, failed_report,
                     errored_report):
    return """%s
test classes: %d
tests run: %d
tests passed: %d
tests failed: %d
tests errored: %d
time: %fms

%s

%s""" % (status, num_test_classes, num_tests_run, num_tests_passed,
         num_tests_failed, num_tests_errored, (finish - start) * 1000,
         failed_report, errored_report)


@transaction.atomic()
def index(request):
    sp1 = transaction.savepoint()
    try:
        start = time.time()
        result_sets = [test_application(app)
                       for app in settings.INSTALLED_APPS]
        finish = time.time()
        all_passed = reduce(
            lambda x, y: x & y, [r.passed() for r in result_sets])
        num_test_classes = sum([r.num_test_classes for r in result_sets])
        num_tests_run = sum([r.num_tests_run for r in result_sets])
        num_tests_passed = sum([r.num_tests_passed for r in result_sets])
        num_tests_failed = sum([r.num_tests_failed for r in result_sets])
        num_tests_errored = sum([r.num_tests_errored for r in result_sets])
        failed_report = make_failed_report(result_sets)
        errored_report = make_errored_report(result_sets)
        if all_passed:
            status = "PASS"
        else:
            status = "FAIL"
        response = HttpResponse(
            plaintext_output(status, num_test_classes, num_tests_run,
                             num_tests_passed, num_tests_failed,
                             num_tests_errored, finish, start, failed_report,
                             errored_report), content_type="text/plain")
        if ('HTTP_ACCEPT' in request.META
                and 'application/json' in request.META['HTTP_ACCEPT']):
            response = HttpResponse(
                json.dumps(
                    dict(
                        status=status,
                        test_classes=num_test_classes,
                        tests_run=num_tests_run,
                        tests_passed=num_tests_passed,
                        tests_failed=num_tests_failed,
                        tests_errored=num_tests_errored,
                        failed_tests=reduce(lambda x, y: x + y,
                                            [r.failed for r in result_sets]),
                        errored_tests=reduce(lambda x, y: x + y,
                                             [r.errored for r in result_sets]),
                        time=(finish - start) * 1000,
                        )),
                content_type="application/json",
                )
    finally:
        transaction.savepoint_rollback(sp1)
    return response
