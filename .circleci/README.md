# CircleCI Configuration
## Environment Variables
There is a minimum acceptable percentage for unit test code coverage that defaults to 85%. 
You can modify this minimum by setting the MIN_COVERAGE_PERCENT environment variable to a 
different value.

# Using CircleCI local CLI

## Install circleci local
Install on Linux or Mac with:
```
curl -fLSs https://raw.githubusercontent.com/CircleCI-Public/circleci-cli/master/install.sh | bash
```

Details and instructions for other platforms in the [CircleCI Docs](https://circleci.com/docs/2.0/local-cli/)

## Validate the config.yml
Run this from the top level of the repo:
```
circleci config validate
```

## Run the CircleCI Job locally
You can run a CircleCI job locally and avoid the change/commit/wait loop you need to
do if you want to actually run the changes on Circle.
This can save a lot of time when trying to debug an issue in CI.
```
circleci local execute --job JOB_NAME
```

##  Environment Variables
To run in the local CircleCI with specific environment variables, use the following pattern:

```
circleci local execute -e MIN_COVERAGE_PERCENT=15 --job unit-test
```

## CircleCI configuration
To get CircleCI to run tests, you have to configure the
project in the Circle web application https://app.circleci.com/
