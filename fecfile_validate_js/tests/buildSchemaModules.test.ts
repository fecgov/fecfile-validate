import { assertEquals } from 'https://deno.land/std/testing/asserts.ts';
import { existsSync } from 'https://deno.land/std/fs/mod.ts';
import * as path from 'https://deno.land/std/path/mod.ts';

const __dirname = path.dirname(path.fromFileUrl(import.meta.url));

const process = Deno.run({ cmd: ['node', 'fecfile_validate_js/scripts/buildSchemaModules'] });
await process.status();

Deno.test({
  name: 'it should create schema *.js files',
  fn: () => {
    const result: boolean = existsSync(`${__dirname}/../dist/F3X.js`);
    assertEquals(result, true);
  },
});

Deno.test({
  name: 'it should create schema *.d.ts files',
  fn: () => {
    const result: boolean = existsSync(`${__dirname}/../dist/F3X.d.ts`);
    assertEquals(result, true);
  },
});
