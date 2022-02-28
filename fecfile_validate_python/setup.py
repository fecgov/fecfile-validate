import setuptools
import shutil
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

print(f"hello{setuptools.find_packages(where='src')}")

print("moving schema files into package")
Path("src/fecfile_validate_python/schema").mkdir(exist_ok=True)
for schema_file in Path("schema").glob("*.json"):
    shutil.copy(schema_file, "src/fecfile_validate_python/schema/")

setuptools.setup(
    name="fecfile-validate",
    version="0.0.1",
    description="A package to validate FECFile Online submissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fecgov/fecfile-validate",
    project_urls={
        "Bug Tracker": "https://github.com/fecgov/fecfile-validate/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where='src'),
    python_requires=">=3.6",
    package_data={"fecfile_validate_python": ['schema/*.json']},
    install_requires=["jsonschema"]
)