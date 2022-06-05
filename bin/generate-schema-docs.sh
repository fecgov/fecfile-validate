#!/bin/bash
#
# Utility script to create the data dictionary *.html files
#
# NOTE: Be sure to run from the fecfile-Validate/schema directory
#
SCHEMAS=$(ls -m *.json | tr -d '[:space:]')
generate-schema-doc ${SCHEMAS} ../docs

# Remove fontawesome script that throws warnings in SonarCloud
sed -e 's/<script src=https:\/\/use\.fontawesome\.com\/facf9fa52c\.js><\/script>//g' -i ../docs/*.html

# Generate spec files
for schema in ${SCHEMAS//,/ }
do
    # call your procedure/other scripts here below
    target_file="${schema%.*}_spec.html"
    python ../bin/generate-spec-table.py $schema > ../docs/$target_file
done