/**
 * Tests for index.ts
 */
import 'jasmine';

import { validate } from './index.js';

describe('validate()', () => {
  it('should return false if empty', () => {
    expect(validate()).toBe(null);
  })
});
