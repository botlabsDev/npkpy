#!/bin/bash

venv=${1:-virtualenv}

## setup virtualenv if not already exist
if [[ ! -e ${venv} ]]; then
  virtualenv --python=python ${venv}
  ${venv}/bin/pip install pip --upgrade
  ${venv}/bin/pip install pip -r requirements-dev.txt
  ${venv}/bin/pip install pip -e .
fi

git config user.name "botlabsDev"
git config user.email "botlabs.dev@botlabs.dev"
echo "--git config--"
echo -n "git user:"; git config user.name
echo -n "git email:"; git config user.email
echo "--------------"

## start virtualenv
source ${venv}/bin/activate





