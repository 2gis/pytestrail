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
    tests = {}
    source_files = __get_source_files(tests_path) if os.path.isdir(tests_path) else [tests_path]
    for filepath in source_files:
        module = imp.load_source('', filepath)
        module_classes = inspect.getmembers(module, predicate=inspect.isclass)
        for module_class in module_classes:
            test_methods = inspect.getmembers(module_class[1], predicate=__istestmethod)
            if len(test_methods) > 0:
                tests[module_class[1]] = test_methods
    return __get_testrail_testcases(tests)


def can_create_testcase(title, suite, section, steps):
    return title is not None and len(title) > 0 \
        and section is not None and len(section) > 0 \
        and suite is not None and len(suite) > 0 \
        and steps is not None and len(steps) > 0


def __get_testrail_testcases(tests):
    testcases = []
    for testclass_obj, tests_list in tests.iteritems():
        default_section = get_section(testclass_obj)
        default_suite = get_suite(testclass_obj)
        for test in tests_list:
            if test[1].__doc__ is not None:
                title = get_test_title(obj=test[1])
                section = get_section(obj=test[1], default_section=default_section)
                suite = get_suite(obj=test[1], default_suite=default_suite)
                steps = get_test_steps(obj=test[1])
                if can_create_testcase(title, suite, section, steps):
                    testcases.append(
                        TestRailTestCase(title=title,
                                         section=section,
                                         suite=suite,
                                         steps=steps)
                    )
    return testcases
