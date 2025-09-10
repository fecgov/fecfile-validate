#!/bin/bash
#
# Utility script to create the index.html file
#
# NOTE: Be sure to run from the fecfile-validate/schema directory
#

python ../bin/generate-index.py

if [ ! -f ../docs/index.html ]; then
    echo "Error: index.html was not generated"
    exit 1
fi;