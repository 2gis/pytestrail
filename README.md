# README #
## What is this repository for? ##

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

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

"""
title: Testcase Example
suite: Testsuite Example
section: Section Example
- Get sixpack
- Get friends
- Get Playstation
= Fun in progress
= Hardcore gaming in progress
"""
```
