import { assertEquals } from 'https://deno.land/std@0.133.0/testing/asserts.ts';
import { validate } from '../dist/index.js';
import { schema as f3xSchema } from '../dist/F3X.js';

const perfectForm_F3X: any = {
  form_type: 'F3XA',
  filer_committee_id_number: 'C00123456',
  committee_name: 'Foes of Chris',
  change_of_address: false,
  street_1: '123 main street',
  street_2: '',
  city: 'Best Town',
  state: 'DC',
  zip: '20000',
  report_code: '',
  election_code: '',
  date_of_election: '20021101',
  state_of_election: 'DC',
  coverage_from_date: '20000101',
  coverage_through_date: '20000201',
  qualified_committee: true,
  treasurer_last_name: 'Doe',
  treasurer_first_name: 'J',
  treasurer_middle_name: 'X',
  treasurer_prefix: 'Dr',
  treasurer_suffix: 'PhD',
  date_signed: '20040729',
  L6b_cash_on_hand_beginning_period: 1,
};

Deno.test({
  name: 'it should pass with perfect data',
  fn: () => {
    const result = validate(f3xSchema, perfectForm_F3X);
    assertEquals(result, []);
  },
});

Deno.test({
  name: 'it should fail without form_type',
  fn: () => {
    const thisData = { ...perfectForm_F3X };
    delete thisData.form_type;
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].keyword, 'required');
    assertEquals(result[0].params.missingProperty, 'form_type');
  },
});

Deno.test({
  name: 'committee_name should allow accents',
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ committee_name: 'Éàñ!@#$%^&*()_+-=[]\\{}|;,./<>?' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "filer_committee_id_number should not be ''",
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ filer_committee_id_number: '' } };
    // TODO: the next line is the goal. Ajv sees '' as a value and we want it to be evaluated as null
    // expect(validate(f3xSchema, thisData).errors).toEqual([ 'filer_committee_id_number should not be empty' ]);
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'filer_committee_id_number');
    assertEquals(result[0].keyword, 'minLength');
    assertEquals(result[0].message, 'must NOT have fewer than 9 characters');
  },
});

Deno.test({
  name: 'filer_committee_id_number is too short',
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ filer_committee_id_number: '12345678' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'filer_committee_id_number');
    assertEquals(result[0].keyword, 'minLength');
    assertEquals(result[0].message, 'must NOT have fewer than 9 characters');
  },
});

Deno.test({
  name: 'filer_committee_id_number is too long',
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ filer_committee_id_number: '1234567890' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'filer_committee_id_number');
    assertEquals(result[0].keyword, 'maxLength');
    assertEquals(result[0].message, 'must NOT have more than 9 characters');
  },
});

Deno.test({
  name: 'filer_committee_id_number violates the pattern',
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ filer_committee_id_number: 'X23456789' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'filer_committee_id_number');
    assertEquals(result[0].keyword, 'pattern');
    assertEquals(result[0].message, 'must match pattern "^[C|P][0-9]{8}$|^[H|S][0-9]{1}[A-Z]{2}[0-9]{5}$"');
  },
});

Deno.test({
  name: 'filer_committee_id_number is required',
  fn: () => {
    const thisData = { ...perfectForm_F3X };
    delete thisData.filer_committee_id_number;
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].keyword, 'required');
    assertEquals(result[0].params.missingProperty, 'filer_committee_id_number');
  },
});

Deno.test({
  name: 'state should be exactly two letters',
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ state: '12X' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[1].keyword, 'pattern');
    assertEquals(result[1].message, 'must match pattern "^[A-Z]{2}$"');
  },
});

Deno.test({
  name: 'state should be only letters',
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ state: '1L' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].keyword, 'pattern');
    assertEquals(result[0].message, 'must match pattern "^[A-Z]{2}$"');
  },
});

Deno.test({
  name: "treasurer_first_name should not be ''",
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ treasurer_first_name: '' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'treasurer_first_name');
    assertEquals(result[0].keyword, 'minLength');
    assertEquals(result[0].message, 'must NOT have fewer than 1 characters');
  },
});

Deno.test({
  name: 'treasurer_first_name is required',
  fn: () => {
    const thisData = { ...perfectForm_F3X };
    delete thisData.treasurer_first_name;
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].keyword, 'required');
    assertEquals(result[0].params.missingProperty, 'treasurer_first_name');
  },
});

Deno.test({
  name: "treasurer_last_name should not be ''",
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ treasurer_last_name: '' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'treasurer_last_name');
    assertEquals(result[0].keyword, 'minLength');
    assertEquals(result[0].message, 'must NOT have fewer than 1 characters');
  },
});

Deno.test({
  name: 'treasurer_last_name is required',
  fn: () => {
    const thisData = { ...perfectForm_F3X };
    delete thisData.treasurer_last_name;
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].keyword, 'required');
    assertEquals(result[0].params.missingProperty, 'treasurer_last_name');
  },
});

Deno.test({
  name: "date_signed should not be ''",
  fn: () => {
    const thisData = { ...perfectForm_F3X, ...{ date_signed: '' } };
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].path, 'date_signed');
    assertEquals(result[0].keyword, 'minLength');
    assertEquals(result[0].message, 'must NOT have fewer than 8 characters');
  },
});

Deno.test({
  name: 'date_signed is required',
  fn: () => {
    const thisData = { ...perfectForm_F3X };
    delete thisData.date_signed;
    const result = validate(f3xSchema, thisData);
    assertEquals(result[0].keyword, 'required');
    assertEquals(result[0].params.missingProperty, 'date_signed');
  },
});
