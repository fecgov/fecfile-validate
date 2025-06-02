import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { existsSync } from "https://deno.land/std/fs/mod.ts";
import * as path from "https://deno.land/std/path/mod.ts";

const __dirname = path.dirname(path.fromFileUrl(import.meta.url));

const command = new Deno.Command("node", {
  args: ["fecfile_validate_js/scripts/buildSchemaModules"],
});
await command.output();

Deno.test({
  name: "it should create schema *.js files",
  fn: async () => {
    const result: boolean = existsSync(`${__dirname}/../dist/8.5/F3X.js`);
    assertEquals(result, true);
  },
});

Deno.test({
  name: "it should create schema *.d.ts files",
  fn: async () => {
    const result: boolean = existsSync(`${__dirname}/../dist/8.5/F3X.d.ts`);
    assertEquals(result, true);
  },
});
