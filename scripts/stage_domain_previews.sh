#!/usr/bin/env bash
set -euo pipefail
# Source is the reviewed, passing central portfolio commit, never a mutable branch.
source_commit='449f214ee483b01607d76bf75363209846d27b94'
output="${1:?Provide a fresh output directory}"
if [[ -e "$output" ]]; then echo 'Output already exists; use a fresh directory' >&2; exit 1; fi
task_source="$(mktemp -d)"
trap 'rm -rf -- "$task_source"' EXIT
git -C "$task_source" init --quiet
git -C "$task_source" fetch --quiet --depth=1 https://github.com/jordanistan/illnetwork.git "$source_commit"
git -C "$task_source" checkout --quiet --detach FETCH_HEAD
python3 "$task_source/portfolio/build.py" --mode preview --output "$output"
python3 "$task_source/portfolio/check.py" "$output"
