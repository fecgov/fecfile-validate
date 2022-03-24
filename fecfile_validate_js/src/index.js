/**
 * Builds the main validator function
 * Compiled into dist/index.js
 * Tested with spec/index-spec.js
 */
const ValidateF3X = require('./validate-F3X');

/**
 * Takes a form id (schemaId) and data object to be validated and returns either false (if there's an error),
 * or an object with errors and warnings arrays
 * @param {string} schemaId
 * @param {object} data
 * @returns {false|object} ajv output of error and warnings ex:
 * {errors: ['field is too long', 'field does not match pattern'], warnings: ['field is recommended']}
 */
function validate(schemaId = '', data = {}) {
  // return false if empty
  if (schemaId != 'F3X' || data == {}) return false;

  // create the function that will return error messages to us
  const ajvValidate = ValidateF3X;
  // test whether the data is valid
  const ajvValid = ajvValidate(data);

  // If there are no errors at all, return true;
  // TODO: need to implement warnings (as opposed to only errors)
  if (ajvValid) return true;
  else {
    let toReturn = {
      errors: [],
      warnings: []
    };
    // console.log('ajvValidate.errors: ', ajvValidate.errors);
    // For every error returned, add their error statements to the list of errors for this function to return
    for (const err of ajvValidate.errors) {
      switch (err.keyword) {
        case 'required':
          toReturn.errors.push(err.message);
          break;
        case 'enum':
          toReturn.errors.push(`${err.instancePath.substring(1)} ${err.message}: [${err.params.allowedValues.join(', ')}]`);
          break;
        case 'pattern':
          toReturn.errors.push(`${err.instancePath.substring(1)} must match its pattern`);
          break;
        default:
          toReturn.errors.push(`${err.instancePath.substring(1)} ${err.message}`);
      }
    }
    return toReturn;
  }
}

module.exports = {
  validate
};
