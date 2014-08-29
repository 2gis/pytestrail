# coding=utf-8
from collections import defaultdict


def get_test_steps(object):
    if object.__doc__ is None:
        return None
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
    if object.__doc__ is None:
        return None
    docstring = object.__doc__.split('\n')
    for str in docstring:
        if str.strip().lower().startswith('section:'):
            section = str[str.find(':') + 1:].strip()
            return section


def get_suite(object):
    if object.__doc__ is None:
        return None
    docstring = object.__doc__.split('\n')
    for str in docstring:
        if str.strip().lower().startswith('suite:'):
            suite = str[str.find(':') + 1:].strip()
            return suite


def get_test_title(object):
    if object.__doc__ is None:
        return None
    docstring = object.__doc__.split('\n')
    name = object.__name__
    for str in docstring:
        if str.strip().lower().startswith('title:'):
            name = str[str.find(':') + 1:].strip()
            break
    return name