#!/bin/bash
#
# Utility script to create the data dictionary *.html files
#
# NOTE: Be sure to run from the fecfile-Validate/schema directory
#E
SCHEMAS=$(ls -m *.json | tr -d ' ')
generate-schema-doc ${SCHEMAS} ../docs
