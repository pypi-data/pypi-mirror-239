#!/usr/bin/env bash

set -e

rm -rf build/ dist/
python3 setup.py sdist bdist_wheel

export TWINE_REPOSITORY_URL=https://upload.pypi.org/legacy/
export TWINE_USERNAME=ssfanli

exec twine upload dist/*