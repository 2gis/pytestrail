# coding=utf-8
import inspect
import os
import imp
import types

from docstring_parser import get_test_steps, get_section, get_suite, get_test_title
from testrail.testcase import TestRailTestCase


def __istestmethod(obj):
    return isinstance(obj, types.MethodType) and obj.__name__.startswith('test')


def __get_source_files(path):
    """
    Returns list of Python source files (*.py) recursively found in :path parameter
    :param path: Path to look for files in
    :return: List of Python source files
    """
    test_files = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if not filename.startswith('__') and filename.endswith('.py'):
                test_files.append(os.path.join(root, filename))
    return test_files


def get_tests(tests_path):
    """
    :param tests_path:
    :return:
    """
    tests_path = os.path.abspath(tests_path)
    tests = set()
    source_files = __get_source_files(tests_path) if os.path.isdir(tests_path) else [tests_path]
    for filepath in source_files:
        module = imp.load_source('', filepath)
        module_classes = inspect.getmembers(module, predicate=inspect.isclass)
        module_tests = []
        for module_class in module_classes:
            module_tests.extend(inspect.getmembers(module_class[1], predicate=__istestmethod))
        tests.update(module_tests)
    return __get_testrail_testcases(tests)


def can_create_testcase(title, suite, section, steps):
    return title is not None and len(title) > 0 \
        and section is not None and len(section) > 0 \
        and suite is not None and len(suite) > 0 \
        and steps is not None and len(steps) > 0


def __get_testrail_testcases(tests):
    testcases = []
    for test in tests:
        if test[1].__doc__ is not None:
            title = get_test_title(test[1])
            section = get_section(test[1])
            suite = get_suite(test[1])
            steps = get_test_steps(test[1])
            if can_create_testcase(title, suite, section, steps):
                testcases.append(
                    TestRailTestCase(title=title,
                                     section=section,
                                     suite=suite,
                                     steps=steps)
                )
    return testcases
