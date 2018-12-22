#!/usr/bin/env bash

set -e
JOB_ID=$1
JSON=$2
WORK_DIR=$3


python image_dl.py $JOB_ID $JSON $WORK_DIR


