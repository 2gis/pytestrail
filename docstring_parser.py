# coding=utf-8
from collections import defaultdict


def get_test_steps(obj):
    if obj.__doc__ is None:
        return None
    docstring = obj.__doc__.split('\n')
    steps = []
    step = defaultdict(lambda: '')
    for docstr in docstring:
        if docstr.strip().startswith('-'):
            if len(step['expected']) > 0:
                steps.append(step)
                step = defaultdict(lambda: '')
            step['content'] += docstr.strip() + '\n'
        if docstr.strip().startswith('ОР') or docstr.strip().startswith('OP'): #or docstr.strip().startswith('='):
            # на всякий случай, ОР написал по-русски и по-английски
            step['expected'] += docstr[docstr.find(':') + 1:].strip() + '\n'
        elif docstr.strip().startswith('='):
            step['expected'] += docstr[docstr.find('=') + 1:].strip() + '\n'
    if len(step['content']) > 0 or len(step['expected']) > 0:
        steps.append(step)
    return steps


def get_section(obj):
    if obj.__doc__ is None:
        return None
    docstring = obj.__doc__.split('\n')
    for docstr in docstring:
        if docstr.strip().lower().startswith('section:'):
            section = docstr[docstr.find(':') + 1:].strip()
            return section


def get_suite(obj):
    if obj.__doc__ is None:
        return None
    docstring = obj.__doc__.split('\n')
    for docstr in docstring:
        if docstr.strip().lower().startswith('suite:'):
            suite = docstr[docstr.find(':') + 1:].strip()
            return suite


def get_test_title(obj):
    if obj.__doc__ is None:
        return None
    docstring = obj.__doc__.split('\n')
    name = obj.__name__
    for docstr in docstring:
        if docstr.strip().lower().startswith('title:'):
            name = docstr[docstr.find(':') + 1:].strip()
            break
    return name