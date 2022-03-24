/**
 * Tests for index.ts
 */

const isProduction = process.env.BUILD === 'production';

// Do we want to test dist or src?
const toTest = isProduction ? '../src/index.js' : '../dist/index.js';
const validate = require(toTest).validate;

const perfectResponse = { errors: [],warnings: [] };

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
beforeAll(() => {
  process.stdout.write(`isProduction: ${isProduction}\n`);
  process.stdout.write(`testing ${toTest}\n`);
});
describe(`validate('F3X')`, () => {
  it('should return false or an empty object', () => {
    expect(validate('')).toBe(false);
  });

  it('should pass with perfect data', () => {
    const expectedResult = validate('F3X', perfectForm_F3X) === true || perfectResponse;
    expect(expectedResult).toEqual(true);
  });
  it('should fail without form_type', () => {
    const thisData = Object.assign({}, perfectForm_F3X);
    delete thisData.form_type;
    expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'form_type\'' ]);
  });
  it('committee_name should allow accents', () => {
    const thisData = Object.assign({}, perfectForm_F3X, { committee_name: 'Éàñ!@#$%^&*()_+-=[]\\{}|;,./<>?' });
    expect(validate('F3X', thisData).errors).not.toEqual([ 'committee_name must match its pattern' ]);
  });
  describe('filer_committee_id_number', () => {
    it('should not be \'\'', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { filer_committee_id_number: '' });
      // TODO: the next line is the goal. Ajv sees '' as a value and we want it to be evaluated as null
      // expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number should not be empty' ]);
      expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number must NOT have fewer than 9 characters' ]);
    });
    it('is too short', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { filer_committee_id_number: '12345678' });
      expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number must NOT have fewer than 9 characters' ]);
    });
    it('is too long', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { filer_committee_id_number: '1234567890' });
      expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number must NOT have more than 9 characters' ]);
    });
    it('violates the pattern', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { filer_committee_id_number: 'X23456789' });
      expect(validate('F3X', thisData).errors).toEqual([ 'filer_committee_id_number must match its pattern' ]);
    });
    it('is required', () => {
      const thisData = Object.assign({}, perfectForm_F3X);
      delete thisData.filer_committee_id_number;
      expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'filer_committee_id_number\'' ]);
    });
  });
  describe('state', () => {
    it('should be exactly two letters', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { state: '12X' });
      expect(validate('F3X', thisData).errors).toEqual([ 'state must NOT have more than 2 characters' ]);
    });
    it('should be only letters', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { state: '1L' });
      expect(validate('F3X', thisData).errors).toEqual([ 'state must match its pattern' ]);
    });
  });

  describe('treasurer_first_name', () => {
    it('should not be \'\'', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { treasurer_first_name: '' });
      // TODO: the next line is the goal. Ajv sees '' as a value and we want it to be evaluated as null
      // expect(validate('F3X', thisData).errors).toEqual([ 'treasurer_first_name should not be empty' ]);
      expect(validate('F3X', thisData).errors).toEqual([ 'treasurer_first_name must NOT have fewer than 1 characters' ]);
    });
    it('is required', () => {
      const thisData = Object.assign({}, perfectForm_F3X);
      delete thisData.treasurer_first_name;
      expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'treasurer_first_name\'' ]);
    });
  });
  describe('treasurer_last_name', () => {
    it('should not be \'\'', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { treasurer_last_name: '' });
      // TODO: the next line is the goal. Ajv sees '' as a value and we want it to be evaluated as null
      // expect(validate('F3X', thisData).errors).toEqual([ 'treasurer_last_name should not be empty' ]);
      expect(validate('F3X', thisData).errors).toEqual([ 'treasurer_last_name must NOT have fewer than 1 characters' ]);
    });
    it('is required', () => {
      const thisData = Object.assign({}, perfectForm_F3X);
      delete thisData.treasurer_last_name;
      expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'treasurer_last_name\'' ]);
    });
  });

  describe('date_signed', () => {
    it('should not be \'\'', () => {
      const thisData = Object.assign({}, perfectForm_F3X, { date_signed: '' });
      // TODO: the next line is the goal. Ajv sees '' as a value and we want it to be evaluated as null
      // expect(validate('F3X', thisData).errors).toEqual([ 'date_signed should not be empty' ]);
      expect(validate('F3X', thisData).errors).toEqual([ 'date_signed must NOT have fewer than 8 characters' ]);
    });
    it('is required', () => {
      const thisData = Object.assign({}, perfectForm_F3X);
      delete thisData.date_signed;
      expect(validate('F3X', thisData).errors).toEqual([ 'must have required property \'date_signed\'' ]);
    });
  });

});
