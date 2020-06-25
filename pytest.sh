#!/bin/bash

pytest --cov=npkpy --cov=tests_acceptance_test -v
pylint --rcfile=.pylintrc npkpy/**
