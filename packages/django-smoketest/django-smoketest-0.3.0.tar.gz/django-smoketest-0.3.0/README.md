django-smoketest
================

[![Build Status](https://travis-ci.org/ccnmtl/django-smoketest.png)](https://travis-ci.org/ccnmtl/django-smoketest)

PLEASE NOTE: I'm basically doing README-driven development here,
writing documentation for how this code should work before actually
implementing it. This notice will go away when django-smoketest is
actually implemented and remotely suitable for real-world use. Until
then, feel free to offer ideas on the interface, but don't expect to
be able to use it (you can look in the "Progress" section to see
exactly where I'm at).

Motivation
----------

Smoke test framework for Django.

Smoke tests are tests that are run on a production environment to
quickly detect major systemic problems. Eg, after you run a deploy,
you want to quickly check that everything is running properly so you
can roll back quickly instead if there are problems. Too often, this
just means visiting the site and manually clicking around through a
few links (at best).

You probably already have unit tests verifying the correctness of low
level parts of your code, and integration and acceptance tests running
on a staging server or CI system. Maybe you've even got automatic
configuration management ensuring that your staging server is
configured as an exact replica of production. So logically, if your
code passes all the tests on the staging server and the production
server is configured the same, everything *must* work right in
production. Right? Wouldn't it be wonderful if the world were so
simple? Of course we know that it's not. That's why we want smoke
tests to actually verify that at least the major components of the
system are all basically functional and able to talk to each other and
we didn't do something stupid like writing code that depends on a new
environment variable that hasn't been set to the correct value on
production yet.

You probably don't want to run your unit tests or integration tests
in production with production settings in effect. Who knows what kind
of insanity would result? Test data sprayed all through your
production database, deleting user data from the file system, the sun
rising in the west and setting in the east?

This is what smoke tests are for. Smoke tests should be *safe* to run
in production. Verify that the application can connect to the
database, that whatever filesystem mounts are expected are in place,
etc. bridging that last gap between existing test coverage and the
wilderness of production. But all while stepping carefully around the
production data.

I also find myself frequently writing small views to support ad-hoc
monitoring. Eg, if an application relies on an NFS mount for some
infrequent operation and that mount has a tendency to go stale, a cron
job that runs every few minutes (or via nagios or some other
monitoring application) and has the application try to read a
file off the mount can help ensure that we are alerted to the stale
mount before users encounter it.

Getting Started
---------------

Install django-smoketest

    $ pip install django-smoketest

Add `smoketest` to your `INSTALLED_APPLICATIONS`.

In each application of yours that you want to define smoke tests for,
make a `smoke.py` file or a `smoke` directory with an
`__init__.py` and one or more python files with your tests.

In your `urls.py`, add something like:

    ('smoketest/', include('smoketest.urls'))

To your `urlpatterns`.

In your `smoke.py` (or module), you put something like this:

    from smoketest import SmokeTest
    from smoketest.decorators import slow, rolled_back
    from myapp.models import FooModel
    
    
    class DemoTest(SmokeTest):
        def test_foomodel_reads(self):
            """ just make sure we can read data from the db """
            cnt = FooModel.objects.all().count()
            self.assertTrue(cnt > 0)
    
        @rolled_back
        def test_foomodel_writes(self):
            """ make sure we can also write to the database
            but do not leave any test detritus around.
            """
            f = FooModel.objects.create()
        
        @slow
        def test_something_slow(self):
            """ this test will not be run in "fast" mode
            because it uses a lot of resources or otherwise
            could bog down the production server in bad ways
            """
            # do a bunch of slow stuff
            # ...
            self.assertEqual(foo, bar)

Now, if you make a `GET` to `http://yourapp/smoketest/`,
django-smoketest will go through your code, finding any `smoke`
modules, and run the tests you have defined (if you've used unittest
or nose, you get the idea), excluding any marked with the `@slow`
decorator. `GET`ing `http://yourapp/smoketest/slow/` will include
those tests as well. All tests passing will result in a response like:

    PASS
    test classes: 1
    tests run: 3
    tests passed: 3
    tests failed: 0
    tests errored: 0
    time: 1200.307861328ms

So you can just check the result for `PASS` if you are calling it from
a monitoring script or as part of an automated deploy.

If tests fail or error out, you instead get something like:

    FAIL
    test classes: 1
    tests run: 8
    tests passed: 5
    tests failed: 2
    tests errored: 1
    time: 3300.07861328ms
    module1.smoke.DemoTest.test_foo failed
    module1.smoke.DemoTest.test_bar failed
    module1.smoke.DemoTest.test_baz errored

If your HTTP client makes the request with `application/json` in the
`Accept:` headers, responses will be JSON objects with the same
information in a more easily parseable form:

    $ curl -H "Accept: application/json" http://yourapp/smoketest/
    {"status": "FAIL", "tests_failed": 2,
     "errored_tests": ["module1.smoke.DemoTest.test_baz"],
     "tests_run": 8, "test_classes": 1, "tests_passed": 5,
     "failed_tests": ["module1.smoke.DemoTest.test_foo",
     "module1.smoke.DemoTest.test_foo"], "tests_errored": 1,
     "time": 1.6458759307861328}

QUESTION: I'm thinking about keeping the output simple to parse
automatically, but maybe we ought to just stick with unittest's
existing output format instead?

API
---

The main class is `smoketests.SmokeTest`, which should be though of as
equivalent to `unittest.TestCase`. It will do basically the usual
stuff there, running `setUp` and `tearDown` methods, and supporting
the usual array of `assertEquals`, `assertRaises`, `assertTrue`
methods.

There is the `@slow` decorator which marks a test as potentially slow,
or utilizing a lot of resources. Either way, it lets you have two
different levels of smoke tests. Fast tests can be run frequently, eg,
from a monitoring script that hits it every five minutes so you can
quickly be alerted if something changes in the production
environment. The `@slow` tests can then be reserved for only running
after a new deploy to check things a little more deeply and have more
confidence that everything is functional.

The `@rolled_back` decorator will make sure that the test gets wrapped
in a database transaction which is then rolled back after
running. This frees you up to do potentially destructive things and
just let the DB clean up for you. The usual caveats apply about making sure
you are using a database that supports transactions and that it can
only roll back database operations, not other side effects. I'm also
on the fence about whether this decorator should even exist or if that
should be the default behavior for all smoke tests. Should a smoke
test ever actually commit a transaction?

In your settings, you may define a `SMOKETEST_APPS` variable that
lists the applications want to run smoke tests from (instead of
looking through all your applications). (do we want a
SMOKETEST_SKIP_APPS as well/instead?).

Asserts supported (so far):

* assertEqual(a, b)
* assertNotEqual(a, b)
* assertTrue(t)
* assertFalse(x)
* assertIs(a, b)
* assertIsNot(a, b)
* assertIsNone(x)
* assertIsNotNone(x)
* assertIn(a, b)
* assertNotIn(a, b)
* assertIsInstance(a, b)
* assertNotIsInstance(a, b)

All call accepts custom message as the last parameter (msg) just like
all assert calls in unittest libraries.


Open Questions
--------------

What other unittest/nose flags, conventions, etc should we support?
`--failfast`? output verbosity? ability to target or skip specific
tests in certain cases? Automatic timeouts (a lot of smoke tests
involve trying to connect to an external service and failing if it
takes more than a specified period of time)?

Progress
--------

TODO:

* @slow decorator and view
* @rolled_back decorator
* capture stdout/stderr
* I think it only handles `smoke.py` files or `smoke/__init__.py` and
  won't yet find subclasses in submodules like `smoke/foo.py`.
* report tracebacks on errors
* setUpClass/tearDownClass
* extended assert* methods (listed in `smoketest/__init__.py`)
* `SMOKETEST_APPS` (and/or `SMOKETEST_SKIP_APPS`)

DONE:

* walk `INSTALLED_APPLICATIONS` and find/run smoke tests
* report numbers in simple text format
* run setUp and tearDown methods
* when tests fail/error, report which ones failed/errored
* proper `module.class.method` info on test failures/errors report
* support the basic expected set of assert* methods from unittest
* JSON output
* time test runs and include in output
* run tests in a rolled back transaction
* report additional info (exception/tracebacks) on errors (Kristijan Mitrovic <kmitrovic>)
* support messages on asserts (Kristijan Mitrovic <kmitrovic>)
