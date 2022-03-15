/**
 * Tests for index.js
 */

// const Jasmine = require('jasmine');
// const jasmine = new Jasmine();
import { validate } from './index';
// const { validate } = require('./index')
// ../dist/fecfile_validate_js/src/index';

describe("expect 1 == 1", () => {
  it("it #1", () => {
    expect(1).toEqual(1);
  });
  it('real test', () => {
    expect(validate()).toEqual(2)
  })
})
