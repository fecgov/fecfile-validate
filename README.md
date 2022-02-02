## About this project
The Federal Election Commission (FEC) is the independent regulatory agency
charged with administering and enforcing the federal campaign finance law.
The FEC has jurisdiction over the financing of campaigns for the U.S. House,
Senate, Presidency and the Vice Presidency.

This project will provide a web application for filling out FEC campaign
finance information. The project code is distributed across these repositories:
- [fecfile-web-app](https://github.com/fecgov/fecfile-web-app): this is the browser-based front-end developed in Angular
- [fecfile-web-api](https://github.com/fecgov/fecfile-web-api): RESTful endpoint supporting the front-end
- [fecfile-validate](https://github.com/fecgov/fecfile-validate): data validation rules and engine
- [fecfile-image-generator](https://github.com/fecgov/fecfile-image-generator): provides competed FEC forms in PDF format

The FEC validator is designed around the disemination of FEC defined data
specifications using the [JSON Schema Specification](http://json-schema.org/).

The initial baseline spec for the definition of each form item is found in
the FEC Format MS Excel spreadsheet found in the FEC Vendor Pack.
(https://www.fec.gov/help-candidates-and-committees/filing-reports/fecfile-software/)
See bin/generate-starter-schema.py for the script that created the initial
schema definition files that were then manually curated and updated.

The data dictionary can be found in a human-freindly HTML format at:
https://fecgov.github.io/fecfile-validate/

### Custom Validation Algorithms
JSON schema properties with a "fec_" prefix are not part of the JSON Schema Standard
but are custom validation enhancements performed by the FEC validation engine in
addition to the validation performed by the JSON Schema Standard validation tools.

- fec_recommended: Array of properties that if the property listed in the array
is missing a value, the validation passes but with a warning issued about the missing value

---

# Deployment (FEC team only)

### Create a feature branch
* Developer creates a feature branch and pushes to `origin`:

    ```
    git checkout develop
    git pull
    git checkout -b feature/my-feature develop
    # Work happens here
    git push --set-upstream origin feature/my-feature
    ```

* Developer creates a GitHub PR when ready to merge to `develop` branch
* Reviewer reviews and merges feature branch into `develop` via GitHub
* [auto] `develop` is deployed to `dev`

### Create a release branch
* Developer creates a release branch and pushes to `origin`:

    ```
    git checkout develop
    git pull
    git checkout -b release/sprint-# develop
    git push --set-upstream origin release/sprint-#
    ```

### Create and deploy a hotfix
* Developer makes sure their local main and develop branches are up to date:

   ```
   git checkout develop
   git pull
   git checkout main
   git pull
   ```

* Developer creates a hotfix branch, commits changes, and **makes a PR to the `main` and `develop` branches**:

    ```
    git checkout -b hotfix/my-fix main
    # Work happens here
    git push --set-upstream origin hotfix/my-fix
    ```

* Reviewer merges hotfix/my-fix branch into `develop` and `main`
* [auto] `develop` is deployed to `dev`. Make sure the build passes before deploying to `main`.
* Developer deploys hotfix/my-fix branch to main using **Deploying a release to production** instructions below

### Deploying a release to production
* Developer creates a PR in GitHub to merge release/sprint-# branch into the `main` branch
* Reviewer approves PR and merges into `main`
* Check CircleCI for passing pipeline tests
* If tests pass, continue
* Delete release/sprint-# branch
* In GitHub, go to `Code -> tags -> releases -> Draft a new release`
* Publish a new release using tag sprint-#, be sure to Auto-generate release notes
* Deploy `sprint-#` tag to production


## Additional developer notes
This section covers a few topics we think might help developers after setup.

### Git Secrets
Set up git secrets to protect oneself from committing sensitive information such as passwords to the repository.
- First install AWS git-secret utility in your PATH so it can be run at the command line: https://github.com/awslabs/git-secrets#installing-git-secrets
- Pull the script to install git-secrets globally on your local machine. This only has to be done one time as you clone the different fecfile github repositories: https://github.com/fecgov/fecfile-web-api/blob/main/install-git-secrets-hook.sh
- Once you have git-secrets installed, run the fecfile-online/install-git-secrets-hook.sh shell script in the root directory of your cloned fecfile-online repo to install the pre-commit hooks.
NOTE: The pre-commit hook is installed GLOBALLY by default so commits to all cloned repositories on your computer will be scanned for sensitive data. See the comments at the top of the script for local install options.
- See git-secrets README for more features: https://github.com/awslabs/git-secrets#readme

### Commit local code changes to origin daily
As a best practice policy, please commit any feature code changes made during the day to origin each evening before signing off for the day.

### Google-style inline documentation
The project is using the Google Python Style Guide as the baseline to keep code style consistent across project repositories.
See here for comment style rules: https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
