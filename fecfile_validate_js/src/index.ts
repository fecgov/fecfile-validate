/**
 * Package that wraps the functionality of the Ajv JSON Schema validator to
 * meet FEC specific use cases.
 *
 * Compiled into dist/index.js
 * Tested with spec/index-spec.js
 */

import { ErrorObject } from "ajv";


/**
 * Validation error information for a single schema property
 * @typedef {object} ValidationError
 * @property {string} path - property name that failed the validation test
 * @property {string} keyword - type of validation check
 * @property {Record<string, any>} params - additional info per the type of validation check
 * @property {string | null} message - human readable message describing validation error
 */
export type ValidationError = {
  path: string;
  keyword: string;
  params: Record<string, any>;
  message: string | null;
};

/**
 * Takes a schema in JSON format and data object to be validated and returns an
 * array of ValidationError objects for all validation errors found by Ajv.
 *
 * @param {object} schema
 * @param {object} data
 * @param {string[]} fieldsToValidate
 * @returns {ValidationError[]} Modified version of Ajv output, empty array if no errors found
 */
export function validate(
  schema: any,
  data: any,
  fieldsToValidate: string[] = []
): Promise<ValidationError[]> {
  const key = schemaToKey(schema);
  return import(`${key} from '../dist/validate-esm.mjs'`).then(module => {
    const isValid: boolean = module(data);
    const retval = isValid ? 'IS VALID!' : 'NOT VALID'; 
    console.log(retval);
    const errors: ValidationError[] = [];
    if (!isValid && !!module.errors?.length) {
      module.errors.forEach((error: any) => {
        const parsedError = parseError(error);
        if (
          !fieldsToValidate.length ||
          fieldsToValidate.includes(parsedError.path)
        ) {
          errors.push(parsedError);
        }
      });
    }
    return errors;
  });
}

/**
 * Format error message from Ajv into our ValidationError interface
 * @param {ErrorObject} error - Ajv ErrorObject interface
 * @returns {ValidationError}
 */
function parseError(error: ErrorObject): ValidationError {
  let path = error.instancePath.substring(1);
  if (error.keyword == "required") {
    path = error.params.missingProperty;
  }
  return {
    path: path,
    keyword: error.keyword,
    params: error.params,
    message: !!error.message ? error.message : null,
  };
}

function schemaToKey(schema: any): string {
  const mappingRegex = ".+/(.+).json$";
  return schema['$id'].match(mappingRegex)[1];
}
