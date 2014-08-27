# coding=utf-8
from collections import defaultdict


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
        if str.lower().startswith('title'):
            name = str[str.find(':') + 1:].strip()
            break
    return name