!/bin/bash

if [ ! -z "$1" ]
then
  clear; echo "test specific file: $1"
  pytest --cov=./ $1 -v
else
  clear; echo "test all project files"
  pytest --cov=npkpy --cov=acceptance_test -v

fi
