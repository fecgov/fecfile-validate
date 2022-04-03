/**
 * Package that wraps the functionality of the Ajv JSON Schema validator to
 * meet FEC specific use cases.
 *
 * Compiled into dist/index.js
 * Tested with spec/index-spec.js
 */

import Ajv, { ValidateFunction } from 'ajv';

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

const ajv = new Ajv({ allErrors: true, strictSchema: false });

/**
 * Takes a schema in JSON format and data object to be validated and returns an
 * array of ValidationError objects for all validation errors found by Ajv.
 *
 * @param {object} schema
 * @param {object} data
 * @returns {ValidationError[]} Modified version of Ajv output, empty array if no errors found
 */
export function validate(schema: any, data: any): ValidationError[] {
  const theSchemaUrl = schema['$schema'];
  schema['$schema'] = theSchemaUrl.replace('https', 'http');

  const validator: ValidateFunction = ajv.compile(schema);
  const isValid: boolean = validator(data);
  const errors: ValidationError[] = [];

  if (!isValid && !!validator.errors) {
    validator.errors.forEach((err) => {
      errors.push({
        path: err.instancePath.substring(1),
        keyword: err.keyword,
        params: err.params,
        message: !!err.message ? err.message : null,
      });
    });
  }

  return errors;
}

// TODO: Validate just one property, will be done in ticket app#189
// ajv.addSchema(schema, schema_name)
// const valid = ajv.validate(`${schema_name}#/properties/${property_name}`, value);
