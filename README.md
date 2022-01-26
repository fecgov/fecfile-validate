The FEC validator is designed around the disemination of FEC defined data
specifications using the [JSON Schema Specification](http://json-schema.org/).

The initial baseline spec for the definition of each form item is found in
the FEC Format MS Excel spreadsheet found in the FEC Vendor Pack.
(https://www.fec.gov/help-candidates-and-committees/filing-reports/fecfile-software/)
See bin/generate-starter-schema.py for the script that created the initial
schema definition files that were then manually curated and updated.

The data dictionary can be found in a human-freindly HTML format at:
https://fecgov.github.io/fecfile-validate/


## About this project
The Federal Election Commission (FEC) is the independent regulatory agency
charged with administering and enforcing the federal campaign finance law.
The FEC has jurisdiction over the financing of campaigns for the U.S. House,
Senate, Presidency and the Vice Presidency.

This project will provide a web application for filling out FEC campaign
finance information. The project code is distributed across these repositories:
- [fecfile-web-app](https://github.com/fecgov/fecfile-web-app): this is the browser-based front-end developed in Angualar
- [fecfile-web-api](https://github.com/fecgov/fecfile-web-api): RESTful endpoint supporting the front-end
- [fecfile-validate](https://github.com/fecgov/fecfile-validate): data validation rules and engine
- [fecfile-image-generator](https://github.com/fecgov/fecfile-image-generator): provides competed FEC forms in PDF format

---

# Deployment (FEC team only)

### Create a changelog
If you're preparing a release to production, you should also create a changelog. The preferred way to do this is using the [changelog generator](https://github.com/skywinder/github-changelog-generator).

Once installed, run:

```
github_changelog_generator --since-tag <last public-relase> --t <your-gh-token>
```

When this finishes, commit the log to the release.

### Creating a new feature
* Developer creates a feature branch and pushes to `origin`:

    ```
    git flow feature start my-feature
    git push origin feature/my-feature
    ```

* Reviewer merges feature branch into `develop` via GitHub
* [auto] `develop` is deployed to `dev`

### Creating a hotfix
* Developer makes sure their local main and develop branches are up to date:

   ```
   git checkout develop
   git pull
   git checkout main
   git pull
   ```

* Developer creates a hotfix branch, commits changes, and **makes a PR to the `main` branch**:

    ```
    git flow hotfix start my-hotfix
    git push origin hotfix/my-hotfix
    ```

* Reviewer merges hotfix branch into `develop` and `main` and pushes to `origin`:

    ```
    git flow hotfix finish my-hotfix
    git checkout develop
    git push origin develop
    ```

* `develop` is deployed to `dev`. Make sure the build passes before deploying to `main`.

    ```
    git checkout main
    git push origin main --follow-tags
    ```

* `main` is deployed to `prod`

### Creating a release
* Developer creates a release branch and pushes to `origin`:

    ```
    git flow release start my-release
    git push origin release/my-release
    ```

* [auto] `release/my-release` is deployed to `stage`
* Issue a pull request to main, tag reviewer(s)
* Review of staging
* Make sure your pull request has been approved
* Make sure local laptop copies of `main`, `develop`, and `release/[release name]` github branches are up-to-date by checking them out and using `git pull` for each branch.
* Rebuild candidate release branch, i.e., `release/sprint-#`, in staging environment, and verify there are no errors and that build passes.
* Developer merges release branch into `main` (and backmerges into `develop`) and pushes to origin:

    ```
    git config --global push.followTags true
    git flow release finish my-release
    ```
    You'll need to save several merge messages, and add a tag message which is named the name of the release (eg., public-beta-20170118). Check to see what `git branch` returns. If it shows you are on `main`, ignore the next step for checking out and pushing to `develop`.
    ```
    git checkout develop
    git push origin develop
    ```
    Watch the develop build on Circle and make sure it passes. Now you are ready to push to prod (:tada:).

    ```
    git checkout main
    git log         # make sure tag for release is present
    git push origin main --follow-tags
    ```
   Watch Circle to make sure it passes, then test the production site manually to make sure everything looks ok.

* `main` is deployed to `prod`
* `develop` is deployed to `dev`

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





