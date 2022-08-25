import os
import sys
import time
import pkg_resources
from inspect import getsourcefile

FRONT_END_ROOT_DIR= "fecfile-web-app"
BACK_END_ROOT_DIR = "fecfile-web-api"
VALIDATOR_ROOT_DIR= "fecfile-validate"
FILE_PATH = os.path.abspath(getsourcefile(lambda: 0))
# Get the directory three steps above the directory containing this file
BASE_DIR = "/".join(FILE_PATH.split("/")[:-3])
YES_TO_ALL = False


def gitpython_is_installed():
    installed_packages = pkg_resources.working_set
    for package in installed_packages:
        if package.key == "gitpython":
            return True
    return False

def get_commit_hash():
    import git
    
    os.chdir(BASE_DIR)
    os.chdir(VALIDATOR_ROOT_DIR)

    repo = git.Repo()
    commit_hash = repo.head.object.hexsha

    print("\nValidator Commit Hash:", commit_hash+"\n")
    sleep(1)

    return commit_hash

def patch_app(commit_hash):
    os.chdir(BASE_DIR)
    os.chdir(FRONT_END_ROOT_DIR)
    os.chdir("front-end")

    print("Patching package.json...")
    sleep(0.5)

    packages = open("package.json", "r")
    package_lines = ""
    for line in packages:
        if "fecfile-validate" in line:
            key, value = line.split(": ")
            url = value.split("#")[0]
            new_line = key+": "+url+"#"+commit_hash+'",\n'
            package_lines += new_line
        else:
            package_lines += line

    packages.close()
    new_packages = open("package.json","w")
    new_packages.write(package_lines)
    new_packages.close()

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

def delete_app_cache():
    print("Deleting .angular & node_modules...")

    os.chdir(BASE_DIR)
    os.chdir(FRONT_END_ROOT_DIR)
    os.chdir("front-end")
    os.system("rm -r .angular")
    os.system("rm -r node_modules")

    print("Done!\nBe sure to run `npm install`\n")
    sleep(0.5)

def delete_api_docker_images(docker_images):
    print("Deleting .angular & node_modules...")
    os.chdir(BASE_DIR)
    os.chdir(BACK_END_ROOT_DIR)
    print("Spinning down Docker...")
    os.system("docker-compose down")
    for image in docker_images:
        print("Removing",image,"...")
        os.system("docker rmi "+image)

    print("Done!\nBe sure to run `docker-compose up`")
    sleep(0.5)

def sleep(T):
    if "-q" not in sys.argv:
      time.sleep(T)

def ask_true_false(question):
    if YES_TO_ALL:
        return True

    response = input(question+" (y/N): ")  
    if (len(response) == 0 or response.upper() not in ["Y","YES"]):
        return False
    return True


def check_user_is_ready():
    print("This script acts upon the active branches of the following repos:")
    for repo in [FRONT_END_ROOT_DIR, BACK_END_ROOT_DIR, VALIDATOR_ROOT_DIR]:
        padded_repo = repo+" "*(48-len(repo))
        print(padded_repo+BASE_DIR+"/"+repo)
    return ask_true_false("\nAre these directories correct?")

def help():
    outString = """

This script uses the active branch of your fecfile-validate repo to update the validator commit hashes of your local app and api repos.  
Optionally, it also deletes the .angular and node_modules directories as well as the relevant docker images.

For this script to work, it needs to be placed in the directory wherein each of the three repos can be found.

Command line arguments:
    -y or --yes |    auto-confirm all options"""
    print(outString)
    return
  
def __main__():
    if "-h" in sys.argv or "--help" in sys.argv:
        help()
        return
    if "-y" in sys.argv or "--yes" in sys.argv:
        YES_TO_ALL = True

    if not gitpython_is_installed():
        print("Please install gitpython!")
        print("python -m pip install gitpython")
        return

    if not check_user_is_ready():
        return
    
    commit_hash = get_commit_hash()
    patch_app(commit_hash)
    patch_api(commit_hash)

    if ask_true_false("Would you like to delete the .angular and node_modules directories within "+FRONT_END_ROOT_DIR):
        delete_app_cache()

    docker_images = ["fecfile-db","fecfile-api","fecfile-celery-worker", "redis:6.2-alpine"]
    if ask_true_false("Would you like to delete the following docker images?\n"+"\n".join(docker_images)+"\n"):
        delete_api_docker_images(docker_images)
    

if __name__ == "__main__":
    __main__()
