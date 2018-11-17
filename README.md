Prvsn
=================

`prvsn` is a simple provisioning tool.

[![Build](https://travis-ci.com/acoomans/prvsn.svg?branch=master)](https://travis-ci.org/acoomans/prvsn)
[![Pypi version](http://img.shields.io/pypi/v/prvsn.svg)](https://pypi.python.org/pypi/prvsn)
[![Pypi license](http://img.shields.io/pypi/l/prvsn.svg)](https://pypi.python.org/pypi/prvsn)
![Python 2](http://img.shields.io/badge/python-2-blue.svg)
![Python 3](http://img.shields.io/badge/python-3-blue.svg)

## Install

	python setup.py install

## Developing

	python setup.py develop
	python setup.py develop --uninstall

## Running tests

	python setup.py test
	
## Goals

Easy to quickly setup a machine for hacking:

- easy to provision a single machine
- works in python
- simple way to
    - add a file, possibly a template
    - install package
    - run a command in bash
- should able to run with minimal python
    - python 2.7 compatibility
    - no external dependencies

## Non-Goals

Large scale provisioning:

- provision thousands or more machines
- strict dependencies, complex dependency graph
- external recipes/supermaket support