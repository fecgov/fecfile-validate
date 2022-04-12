## Developer Notes

The FEC javascript validation package is a wrapper around the Ajv schema validation
package (https://ajv.js.org/) with additional checks specific to FEC business rules.

The package is distributed through the npm package management system and is, currently,
only provided directly from the GitHub repo.

To install the validation package, add this line to your package.json dependencies:

"fecfile-validate": "https://github.com/fecgov/fecfile-validate#develop"

## API

function validate(schema, data)

Returns an array of errors or an empty array if none are found.

Validation error information for a single schema property:
```
 @typedef {object} ValidationError
 @property {string} path - property name that failed the validation test
 @property {string} keyword - type of validation check
 @property {Record<string, any>} params - additional info per the type of validation check
 @property {string | null} message - human readable message describing validation error
 ```

Error example:
```
[{
    keyword: "required",
    message: "must have required property 'form_type'",
    params: {
        missingProperty: "form_type",
    },
    path: "",
}]
```

## Testing

The test runner being used for the *.ts files is the native testing suite found in Deno (https://deno.land)

To install Deno: https://deno.land/#installation

Deno testing: https://deno.land/manual@v1.20.4/testing
