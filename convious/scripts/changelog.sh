#!/bin/sh

set -ex

latest_tag=$(git describe --tags --abbrev=0)

git log --pretty=oneline --abbrev-commit "$latest_tag..HEAD"
