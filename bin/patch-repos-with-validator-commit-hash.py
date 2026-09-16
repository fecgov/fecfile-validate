import os
import time
import json
import argparse
from inspect import getsourcefile


FRONT_END_ROOT_DIR = "fecfile-web-app"
BACK_END_ROOT_DIR = "fecfile-web-api"
VALIDATOR_ROOT_DIR = "fecfile-validate"
FILE_PATH = os.path.abspath(getsourcefile(lambda: 0))
# Get the directory three steps above the directory containing this file
BASE_DIR = "/".join(FILE_PATH.split("/")[:-3])
YES_TO_ALL = False
QUICK = False


def get_commit_hash_automatic():
    import git

    os.chdir(BASE_DIR)
    os.chdir(VALIDATOR_ROOT_DIR)

    repo = git.Repo()
    return repo.head.object.hexsha


def get_commit_hash_manual(skip_gitpython_install_recommendation):
    if not skip_gitpython_install_recommendation:
        print(
            "\n\n"
            "This script can optionally use the gitpython module to automatically\n"
            "retrieve the most recent commit hash of your validate repo's active branch"
            "\n\n"
            "You can install it with: python -m pip install gitpython\n"
            "\n\n"
            "Alternatively:"
        )

    return input("Please input the commit hash: ")


def get_commit_hash():
    try:
        print("\n\nAttempting to automatically retrieve commit hash...")
        commit_hash = get_commit_hash_automatic()

        sleep(1)
        print("\nValidator Commit Hash:", commit_hash+"\n")
        correct = ask_true_false("Is this correct?")
        if correct:
            return commit_hash
        else:
            return get_commit_hash_manual(True)
    except ModuleNotFoundError:
        print("Failed to automatically retrieve commit hash")
        return get_commit_hash_manual(YES_TO_ALL)


def patch_app(commit_hash):
    os.chdir(BASE_DIR)
    os.chdir(FRONT_END_ROOT_DIR)
    os.chdir("front-end")

    print("Patching package.json...")
    sleep(0.5)

    package = open("package.json", "r")
    package_manifest = json.load(package)
    package.close()

    package_manifest["dependencies"]["fecfile-validate"] = (
        f"https://github.com/fecgov/fecfile-validate#{commit_hash}"
    )

    allow_scripts = package_manifest["allowScripts"]
    allow_script_keys = allow_scripts.keys()

    new_allowed_scripts = {}
    for allow_script_key in allow_script_keys:
        if "fecfile-validate" in allow_script_key:
            script_name = f"github:fecgov/fecfile-validate#{commit_hash}"
            new_allowed_scripts[script_name] = allow_scripts[allow_script_key]
        else:
            new_allowed_scripts[allow_script_key] = allow_scripts[allow_script_key]

    package_manifest["allowScripts"] = new_allowed_scripts

    package = open("package.json", "w")
    json.dump(
        package_manifest,
        package,
        indent=2,
    )
    package.write("\n")
    package.close()

    print("Done!\n")
    sleep(0.5)


def patch_api(commit_hash):
    os.chdir(BASE_DIR)
    os.chdir(BACK_END_ROOT_DIR)

    print("Patching requirements.txt...")
    sleep(0.5)

    new_requirements = ""
    requirements_file = open("requirements.txt", "r")
    for line in requirements_file:
        if "fecfile-validate" in line:
            url = line.split("@")[0]
            parameters = line.split("#")[1]
            new_line = url+"@"+commit_hash+"#"+parameters
            new_requirements += new_line
        else:
            new_requirements += line

    requirements_file.close()
    new_requirements_file = open("requirements.txt", "w")
    new_requirements_file.write(new_requirements)
    new_requirements_file.close()

    print("Done!\n")
    sleep(0.5)


def sleep(t):
    if not QUICK:
        time.sleep(t)


def ask_true_false(question):
    if YES_TO_ALL:
        return True

    response = input(question+" (y/N): ")
    if (len(response) == 0 or response.upper() not in ["Y", "YES"]):
        return False
    return True


def check_directories_are_correct():
    print("This script acts upon the active branches of the following repos:")
    for repo in [FRONT_END_ROOT_DIR, BACK_END_ROOT_DIR, VALIDATOR_ROOT_DIR]:
        padded_repo = repo+" "*(48-len(repo))
        print(padded_repo+BASE_DIR+"/"+repo)
    return ask_true_false("\nAre these directories correct?")


def main():
    description = (
        "This script updates the validator commit hash in fecfile-web-api's\n"
        "requirements.txt file and in fecfile-web-app's package.json file.\n\n"
        "If the gitpython module is installed, this script will automatically\n"
        "retrieve the commit hash for the most recent commit on the working\n"
        "branch of your fecfile-validate repo.  Alternatively, you can enter\n"
        "the commit hash manually."
    )

    parser = argparse.ArgumentParser(
        prog="patch-repos-with-validator-commit-hash",
        description=description,
    )

    parser.add_argument(
        '-y',
        '--yes',
        action="store_true",
        default=False,
        help="auto-confirm all y/n prompts"
    )
    parser.add_argument(
        '-q',
        '--quick',
        action="store_true",
        default=False,
        help="Skip all sleep() calls"
    )

    args = parser.parse_args()
    if args.yes:
        global YES_TO_ALL
        YES_TO_ALL = True
    if args.quick:
        global QUICK
        QUICK = True

    if not check_directories_are_correct():
        return

    commit_hash = get_commit_hash()
    patch_app(commit_hash)
    patch_api(commit_hash)


if __name__ == "__main__":
    main()
