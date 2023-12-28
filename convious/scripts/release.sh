#!/bin/sh

set -ex

case $1 in
  --major) awk_script='{print $1+1 "." 0 "." 0}' ;;
  --minor) awk_script='{print $1 "." $2+1 "." 0}' ;;
  ''|--patch) awk_script='{print $1 "." $2 "." $3+1}' ;;
esac

git checkout master
git pull
git tag \
  | grep -v test \
  | sort -rV \
  | grep '\.' \
  | head -n1 \
  | tr '.' ' ' \
  | awk "$awk_script" \
  | xargs git tag
git push
git push --tags
