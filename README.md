# README #
A simple app to import unittest autotests into TestRail.

## Command Line Parameters (unittestrail.py) ##
* __--project (-p)__ TestRail project id (number)

* __--base_url (-H)__ TesRail address. http://testrail.local/ for example

* __--login (-l)__ TestRail username

* __--password (-P)__ User`s password

* __--tests_dir (-d)__ Directory with tests to import 

* __--delete_tests (-D)__ Deletes all tests from TestRail that was deleted from Python files

## Tests Description ##
In all docstrings in tests you want to import into TestRail must start with following strings:

* __title:__ Test title which appears in TestRail as testcase`s name (will take test method name if title: is not presented)

* __suite:__ Testsuite name (required, will be created if not presented)

* __section:__ Section name in defined suite (required, will be created if not presented)

### Steps description ###
Each step must start with a dash (-). After any amount of steps may be expected result: a s tring(s) which starts with equals sign (=)

## Example ##

```
#!python

def test_party(self):
    """
    title: Testcase Example
    suite: Testsuite Example
    section: Section Example
    - Get sixpack
    - Get friends
    = Fun in progress
    - Get Playstation
    = Hardcore gaming in progress
    """
    pass
```