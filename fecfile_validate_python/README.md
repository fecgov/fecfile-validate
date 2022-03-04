# FECFile Validate Python

This is a package to validate FECFile Online submissions

To install with pip:
`pip install "git+https://github.com/fecgov/fecfile-validate@main#egg=fecfile_validate&subdirectory=fecfile_validate_python"`

To include in requirements.txt add this line:
`git+https://github.com/fecgov/fecfile-validate@main#egg=fecfile_validate&subdirectory=fecfile_validate_python`

# Example

```
from fecfile_validate import validate

form_data = ...
validation_result = validate.validate("F3X", form_data)
print(validation_result.errors) # prints [] of ValidationErrors
```
