#!/bin/bash
#
# Utility script to perform mass updates to the schema file.
# NOTE: Be sure to run from the fecfile-Validate/schema directory
#
import glob
import json


def process(file, schema):
  print('*** ' + file)
  if 'filer_committee_id_number' in schema['properties']:
    schema['properties']['filer_committee_id_number']['pattern'] = '^[C|P][0-9]{8}$|^[H|S][0-9]{1}[A-Z]{2}[0-9]{5}$'
    schema['properties']['filer_committee_id_number']['fec_spec']['RULE_REFERENCE'] = 'this is the ID of the Committee Account the report/transaction is associated with'
  if 'transaction_id' in schema['properties']:
    schema['properties']['transaction_id']['fec_spec']['RULE_REFERENCE'] = 'Must be unique for the life of a report (original + amendments) within each committee account. Letters, if included, must be uppercase.'
  if 'contribution_date' in schema['properties']:
    schema['properties']['contribution_date']['type'] = 'string'
  return schema


for file in (glob.glob('*.json') + glob.glob('backlog/*.json')):
  
  f = open(file)
  schema = json.load(f)
  f.close()
  
  schema = process(file, schema)

  f = open(file, 'w')
  json.dump(schema, f, indent=4)
  f.close()



