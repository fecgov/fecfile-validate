#!/bin/bash

# curl -F ‘data=@1525984.fec’ localhost:8001/v1/validate

curl \
    -F "form_type=F99" \
    -F "json_validate=@1525984.fec" \
    http://localhost:8001/v1/validate