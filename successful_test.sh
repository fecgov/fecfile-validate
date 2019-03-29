#!/bin/bash

text_file="reports/$1-$2-flake8.txt"
xml_file="reports/$1-$2-flake8_junit.xml"

project_dir="."

virtualenv -p python3.7 .venv
source .venv/bin/activate
pip3 install flake8 flake8-junit-report pep8 pep8-naming
mkdir -p reports
flake8 --exit-zero $project_dir --output-file $text_file
flake8_junit $text_file $xml_file 
deactivate

if [ ! -s $text_file ]; then
  count=$( find . -type f -name "*.py" | grep -v '.venv' | wc -l )
  echo '<testsuite errors="0" failures="0" name="flake8" tests="'$count'" time="1">'
  for i in $( find . -type f -name "*.py" | grep -v '.venv' );do
    echo '<testcase name="'$i'"></testcase>' >> $xml_file
  done
  echo "</testsuite>" >> $xml_file

fi
rm -fr .venv