#!/usr/bin/env bash

set -e

IMAGE_DIR=$1
RESULTS_FILE=$2


python image_dl.py --image_dir $IMAGE_DIR \
--results-file $RESULTS_FILE
