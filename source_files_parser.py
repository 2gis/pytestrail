# coding=utf-8
from collections import defaultdict
import inspect
import os
import imp
import types
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
    Gets list of tuples ('testName', testMethod) in :tests_dir recursively
    :param tests_dir:
    :return:
    """
    tests = set()
    for file in __get_source_files(tests_dir):
        module = imp.load_source('', file)
        module_classes = inspect.getmembers(module, predicate=inspect.isclass)
        module_tests = []
        for module_class in module_classes:
            module_tests.extend(inspect.getmembers(module_class[1], predicate=__istestmethod))
        tests.update(module_tests)
        get_testrail_testcases(tests)
    return get_testrail_testcases(tests)


def get_testrail_testcases(tests):
    testcases = []
    for test in tests:
        if test[1].__doc__ is not None:
            testcases.append(
                TestRailTestCase(get_test_name(test[1]),
                                 get_section(test[1]),
                                 get_suite(test[1]),
                                 get_test_steps(test[1])
                )
            )
    return testcases


def get_section(object):
    docstring = object.__doc__.split('\n')
    docstring[0] = 'section: section name'
    for str in docstring:
        if str.lower().startswith('section'):
            section = str[str.find(':') + 1:].strip()
            return section


def get_suite(object):
    docstring = object.__doc__.split('\n')
    docstring[0] = 'suite: suite name'
    for str in docstring:
        if str.lower().startswith('suite'):
            suite = str[str.find(':') + 1:].strip()
            return suite


def get_test_name(object):
    docstring = object.__doc__.split('\n')
    name = object.__name__
    for str in docstring:
        if str.lower().startswith('name'):
            name = str[str.find(':') + 1:].strip()
            break
    return name

def get_test_steps(object):
    docstring = object.__doc__.split('\n')
    steps = []
    step = defaultdict(lambda : '')
    for str in docstring:
        if str.strip().startswith('-'):
            if len(step['expected']) > 0:
                steps.append(step)
                step = defaultdict(lambda : '')
            step['content'] += str.strip() + '\n'
        if str.strip().startswith('ОР') or str.strip().startswith('OP'):
            # на всякий случай, ОР написал по-русски и по-английски
            step['expected'] += str.strip() + '\n'
    if len(step['content']) > 0 or len(step['expected']) > 0:
        steps.append(step)
    return steps
