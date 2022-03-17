/**
 * Tests for index.js
 */
import 'jasmine';

import { validate } from './index';

describe("expect 1 == 1", () => {
  it("it #1", () => {
    expect(1).toEqual(2);
  });
  it('real test', () => {
    expect(validate()).not.toBeDefined()
  })
})
