# coding=utf-8
import inspect
import os
import imp
import types

from docstring_parser import get_test_steps, get_section, get_suite, get_test_title
from testrail.testcase import TestRailTestCase


def __istestmethod(object):
    return isinstance(object, types.MethodType) and object.__name__.startswith('test')


def __get_source_files(path):
    """
    Returns list of Python source files (*.py) recursively found in :path parameter
    :param path: Path to look for files in
    :return: List of Python source files
    """
    test_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.startswith('__') and file.endswith('.py'):
                test_files.append(os.path.join(root, file))
    return test_files


def get_tests(tests_dir):
    """
    Gets list of testcases in :tests_dir recursively
    :param tests_dir:
    :return:
    """
    tests_dir = os.path.abspath(tests_dir)
    tests = set()
    for file in __get_source_files(tests_dir):
        module = imp.load_source('', file)
        module_classes = inspect.getmembers(module, predicate=inspect.isclass)
        module_tests = []
        for module_class in module_classes:
            module_tests.extend(inspect.getmembers(module_class[1], predicate=__istestmethod))
        tests.update(module_tests)
    return __get_testrail_testcases(tests)


def __get_testrail_testcases(tests):
    testcases = []
    for test in tests:
        if test[1].__doc__ is not None:
            testcases.append(
                TestRailTestCase(get_test_title(test[1]),
                                 get_section(test[1]),
                                 get_suite(test[1]),
                                 get_test_steps(test[1])
                )
            )
    return testcases
