/**
 * Tests for index.ts
 */
const validate = require('../src/index.js').validate;

const noErrorsNoWarnings = {errors: [],warnings: []};

const perfectForm_F3X = {
  'form_type': 'F3XA',
  'filer_committee_id_number': 'C00123456',
  'committee_name': 'Foes of Chris',
  'change_of_address': false,
  'street_1': '123 main street',
  'street_2': '',
  'city': 'Best Town',
  'state': 'DC',
  'zip': '20000',
  'report_code': '',
  'election_code': '',
  'date_of_election': '20021101',
  'state_of_election': 'DC',
  'coverage_from_date': '20000101',
  'coverage_through_date': '20000201',
  'qualified_committee': true,
  'treasurer_last_name': 'Doe',
  'treasurer_first_name': 'J',
  'treasurer_middle_name': 'X',
  'treasurer_prefix': 'Dr',
  'treasurer_suffix': 'PhD',
  'date_signed': '20040729',
  'L6b_cash_on_hand_beginning_period': 1
};

describe('validate(\'F3X\')', () => {
  it('should return false or an empty object', () => {
    expect(validate('')).toBe(false);
  });
  it('should pass with perfect data', () => {
    const expectedResult = validate('F3X', perfectForm_F3X) == true || noErrorsNoWarnings;
    expect(expectedResult).toEqual(true);
  });
  it('should fail without form_type', () => {
    const thisData = Object.assign({}, perfectForm_F3X);
    delete thisData.form_type;
    expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'form_type\'' ]);
  });
  it('should fail with filer_committee_id_number of \'\'', () => {
    const thisData = Object.assign({}, perfectForm_F3X, {filer_committee_id_number: ''});
    expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number should not be empty' ]);
  });
  it('should fail if filer_committee_id_number is too short', () => {
    const thisData = Object.assign({}, perfectForm_F3X, {filer_committee_id_number: '12345678'});
    expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number must NOT have fewer than 9 characters' ]);
  });
  it('should fail with filer_committee_id_number is too long', () => {
    const thisData = Object.assign({}, perfectForm_F3X, {filer_committee_id_number: '1234567890'});
    expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number must NOT have more than 9 characters' ]);
  });
  it('should fail without filer_committee_id_number', () => {
    const thisData = Object.assign({}, perfectForm_F3X);
    delete thisData.filer_committee_id_number;
    expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'filer_committee_id_number\'' ]);
  });
});
