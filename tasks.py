import git
import json
import os
import sys

from invoke import task


APP_NAME = "fecfile-validate"
ORG_NAME = "fec-fecfileonline-prototyping"


def _detect_space(repo, branch=None):
    """Detect space from active git branch.
    :param str branch: Optional branch name override
    :returns: Space name if space is detected and confirmed, else `None`
    """
    space = _resolve_rule(repo, branch)
    if space is None:
        print("No space detected")
        return None
    print("Detected space {space}".format(**locals()))
    return space


def _detect_prod(repo, branch):
    """Deploy to production if master is checked out and tagged."""
    if branch != "master":
        return False
    try:
        # Equivalent to `git describe --tags --exact-match`
        repo.git().describe("--tags", "--exact-match")
        return True
    except git.exc.GitCommandError:
        return False


def _resolve_rule(repo, branch):
    """Get space associated with first matching rule."""
    for space, rule in DEPLOY_RULES:
        if rule(repo, branch):
            return space
    return None


def _detect_branch(repo):
    try:
        return repo.active_branch.name
    except TypeError:
        return None


DEPLOY_RULES = (
    ("prod", _detect_prod),
    ("stage", lambda _, branch: branch.startswith("release")),
    # ("dev", lambda _, branch: branch == "develop"),
    ("dev", lambda _, branch: branch == "test-cloud-gov-deploy"),
)


SPACE_URLS = {
    "dev": [("app.cloud.gov", "fecfile-dev-validate")],
    "stage": [("app.cloud.gov", "fecfile-stage-validate")],
    "prod": [("app.cloud.gov", "fecfile-prod-validate")],
}


@task
def deploy(ctx, space=None, branch=None, login=None):
    """Deploy app to Cloud Foundry.
    Log in using credentials stored per environment
    like `FEC_CF_USERNAME_DEV` and `FEC_CF_PASSWORD_DEV`;
    Push to either `space` or the space detected from the name and tags
    of the current branch.
    Note: Must pass `space` or `branch` if repo is in detached HEAD mode,
    e.g. when running on Circle.

    Example usage: invoke deploy --space dev
    """
    # Detect space
    repo = git.Repo(".")
    branch = branch or _detect_branch(repo)
    space = space or _detect_space(repo, branch)
    if space is None:
        return

    if login == "True":
        # Set api
        api = "https://api.fr.cloud.gov"
        ctx.run("cf api {0}".format(api), echo=True)
        # Authenticate
        login_command = 'cf auth "$FEC_CF_USERNAME_{0}" "$FEC_CF_PASSWORD_{0}"'.format(
            space.upper()
        )
        ctx.run(login_command, echo=True)

    # Target space
    ctx.run("cf target -o {0} -s {1}".format(ORG_NAME, space), echo=True)

    # Set deploy variables
    with open(".cfmeta", "w") as fp:
        json.dump({"user": os.getenv("USER"), "branch": branch}, fp)

    # Deploy application
    existing_deploy = ctx.run("cf app {0}".format(APP_NAME), echo=True, warn=True)
    print("\n")
    cmd = "push --strategy rolling" if existing_deploy.ok else "push"
    new_deploy = ctx.run(
        "cf {cmd} {app} -f manifest-{space}.yml".format(
            cmd=cmd, app=APP_NAME, space=space
        ),
        echo=True,
        warn=True,
    )

    if not new_deploy.ok:
        print("Build failed!")
        # Check if there are active deployments
        app_guid = ctx.run("cf app {} --guid".format(APP_NAME), hide=True, warn=True)
        app_guid_formatted = app_guid.stdout.strip()
        status = ctx.run(
            'cf curl "/v3/deployments?app_guids={}&status_values=ACTIVE"'.format(
                app_guid_formatted
            ),
            hide=True,
            warn=True,
        )
        active_deployments = (
            json.loads(status.stdout).get("pagination").get("total_results")
        )
        # Try to roll back
        if active_deployments > 0:
            print("Attempting to roll back any deployment in progress...")
            # Show the in-between state
            ctx.run("cf app {}".format(APP_NAME), echo=True, warn=True)
            cancel_deploy = ctx.run(
                "cf cancel-deployment {}".format(APP_NAME), echo=True, warn=True
            )
            if cancel_deploy.ok:
                print("Successfully cancelled deploy. Check logs.")
            else:
                print("Unable to cancel deploy. Check logs.")

        return sys.exit(1)

        print(
            "\nA new version of your application '{}' has been successfully pushed!".format(
                APP_NAME
            )
        )
        ctx.run("cf apps", echo=True, warn=True)

    # Needed for CircleCI
    return sys.exit(0)
