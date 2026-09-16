import os
import sys
import time
import json
from inspect import getsourcefile


FRONT_END_ROOT_DIR = "fecfile-web-app"
BACK_END_ROOT_DIR = "fecfile-web-api"
VALIDATOR_ROOT_DIR = "fecfile-validate"
FILE_PATH = os.path.abspath(getsourcefile(lambda: 0))
# Get the directory three steps above the directory containing this file
BASE_DIR = "/".join(FILE_PATH.split("/")[:-3])
YES_TO_ALL = False


def get_commit_hash_automatic():
    import git

    os.chdir(BASE_DIR)
    os.chdir(VALIDATOR_ROOT_DIR)

    repo = git.Repo()
    return repo.head.object.hexsha


def get_commit_hash_manual(skip_gitpython_install_recommendation=True):
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
    except:
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

    allowedScripts = package_manifest["allowScripts"].keys()

    newAllowedScripts = {}
    for allowedScript in allowedScripts:
        if "fecfile-validate" in allowedScript:
            scriptName = f"github:fecgov/fecfile-validate#{commit_hash}"
            newAllowedScripts[scriptName] = package_manifest["allowScripts"][allowedScript]
        else:
            newAllowedScripts[allowedScript] = package_manifest["allowScripts"][allowedScript]

    package_manifest["allowScripts"] = newAllowedScripts

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
    if "-q" not in sys.argv:
        time.sleep(t)


def ask_true_false(question):
    if YES_TO_ALL:
        return True

    response = input(question+" (y/N): ")
    if (len(response) == 0 or response.upper() not in ["Y", "YES"]):
        return False
    return True


def check_user_is_ready():
    print("This script acts upon the active branches of the following repos:")
    for repo in [FRONT_END_ROOT_DIR, BACK_END_ROOT_DIR, VALIDATOR_ROOT_DIR]:
        padded_repo = repo+" "*(48-len(repo))
        print(padded_repo+BASE_DIR+"/"+repo)
    return ask_true_false("\nAre these directories correct?")


def help():
    help_string = """
        This script updates the validator commit hash in fecfile-web-api's requirements.txt file 
        and in fecfile-web-app's package.json file.  If the gitpython module is installed, this 
        script will automatically retrieve the commit hash for the most recent commit on the 
        working branch of your fecfile-validate repo.  Alternatively, you can manually enter the 
        commit hash.

        Command line arguments:
            -y or --yes |    auto-confirm all options
            -q          |    skip all sleep() calls
    """
    print(help_string)


def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        return help()
    if "-y" in sys.argv or "--yes" in sys.argv:
        global YES_TO_ALL
        YES_TO_ALL = True

    if not check_user_is_ready():
        return

    commit_hash = get_commit_hash()
    patch_app(commit_hash)
    patch_api(commit_hash)


if __name__ == "__main__":
    main()
