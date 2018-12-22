#!/usr/bin/env bash

set -e
JOB_ID=$1
JSON=$2
IMAGE_DIR=$3
RESULTS_FILE=$4



python image_dl.py $JOB_ID $JSON $IMAGE_DIR $RESULTS_FILE
