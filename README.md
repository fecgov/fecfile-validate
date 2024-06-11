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

*Special Note:* The requirements.txt field in the fecfile-web-api repo must be updated with the most recent commit hash for the commit changes to be pulled into the api build by CircleCI.

### Create a feature branch

Using git-flow extensions:
    ```
    git flow feature start feature_branch
    ```

Without the git-flow extensions:
    ```
    git checkout develop
    git pull
    git checkout -b feature/feature_branch develop
    ```

* Developer creates a GitHub PR when ready to merge to `develop` branch
* Reviewer reviews and merges feature branch into `develop` via GitHub

### Create a release branch

* Using git-flow extensions:
```
git flow release start sprint-#
```

* Without the git-flow extensions:
```
git checkout develop
git pull
git checkout -b release/sprint-# develop
git push --set-upstream origin release/sprint-#
```
* Developer creates a PR in GitHub to merge release/sprint-# branch into the `main` branch to track if commits pass deployment checks. The actual merge will happen when deploying a release to production.

### Create and deploy a hotfix

* Using git-flow extensions:
```
git flow hotfix start my-fix
# Work happens here
git flow hotfix finish my-fix
```

* Without the git-flow extensions:
```
git checkout -b hotfix/my-fix main
# Work happens here
git push --set-upstream origin hotfix/my-fix
```

* Developer creates a hotfix branch, commits changes, and **makes a PR to the `main` and `develop` branches**:
* Reviewer merges hotfix/my-fix branch into `develop` and `main`
* Developer deploys hotfix/my-fix branch to main using **Deploying a release to production** instructions below

### Deploying a release to production
* Reviewer approves PR and merges into `main`
* Check CircleCI for passing pipeline tests
* If tests pass, continue
* (If commits were made to release/sprint-#) Developer creates a PR in GitHub to merge release/sprint-# branch into the `develop` branch
* Reviewer approves PR and merges into `develop`
* Delete release/sprint-# branch
* Publish a new release using tag sprint-#, be sure to Auto-generate release notes
  * On Github, click on "Code" tab, then the "tags" link, then the "Releases" toggle
  * Click the button "Draft a new release"
  * Enter the new sprint tag "sprint-XX"
  * Set Target option to "main"
  * Set Release title to "sprint-XX"
  * Click the button "Generate release notes"
  * Click the "Publish release" button


## Additional developer notes
This section covers a few topics we think might help developers after setup.

### Register changes to the validation JSON files in the fecfile-web-app and fecfile-web-api repositories
After modified the JSON schema files, those changes must be registered in the [fecfile-web-app](https://github.com/fecgov/fecfile-web-app) and [fecfile-web-api](https://github.com/fecgov/fecfile-web-api) repositories using the hash of the commit of the edits.

In the fecfile-web-app repo:
1) Update the commit hash in the [package.json](https://github.com/fecgov/fecfile-web-app/blob/develop/front-end/package.json) file for the fecfile-validate dependency
2) Remove the package-lock.json file
3) Rebuild the package-lock.json file to commit it to the repo with the "npm install" command

In the fecfile-web-api repo:
1) Update the commit hash for the fecfile-validate dependency in the [requirements.txt](https://github.com/fecgov/fecfile-web-api/blob/develop/requirements.txt) file.

### How to update the online documentation
The online documentation for the validation JSON files is hosted on GitHub pages at https://fecgov.github.io/fecfile-validate/
To update this documentation when changes are made to the JSON validation files, we use the [json-schema-for-humans](https://pypi.org/project/json-schema-for-humans/) python package. To generate the documentation, follow these steps:
1) pip install -r requirements.txt
2) cd schema
3) ../bin/generate_schema_docs.sh

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
