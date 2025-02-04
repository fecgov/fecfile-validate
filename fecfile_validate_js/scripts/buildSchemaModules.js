/**
 * Script to create optimized ES Module import files for each schema JSON file.
 * This script is run as part of the build process and at postinstall.
 */

import Ajv from 'ajv';
import standaloneCode from 'ajv/dist/standalone/index.js';
import * as fs from 'fs';
import glob from 'glob';
import * as path from 'path';
import * as url from 'url';

const dir = path.dirname(url.fileURLToPath(import.meta.url));
fs.mkdirSync(path.join(dir, `../dist`), { recursive: true });
const files = glob.sync(path.join(dir, '../../schema/*.json'));
let schemaNamesExport = "export enum SchemaNames {";

for (const file of files) {
  const schema = JSON.parse(fs.readFileSync(file, 'utf-8'));
  const key = schemaToKey(schema);
  delete schema.$schema;
  delete schema.$id;
  delete schema.version;
  delete schema.title;
  delete schema.description;
  delete schema.fec_recommended;

  for (let n in schema.properties) {
    delete schema.properties[n].title;
    delete schema.properties[n].description;
    delete schema.properties[n].examples;
    delete schema.properties[n].fec_spec;
  }

  const typeExports = `export declare function ${key}(data: any, options: any): boolean;`
  const ajv = new Ajv({ code: { source: true, esm: true } });
  const validate = ajv.compile(schema);
  const moduleCode = standaloneCode(ajv, validate)
  fs.writeFileSync(path.join(dir, `../dist/${key}.mjs`), moduleCode);
  fs.writeFileSync(path.join(dir, `../dist/${key}.d.mts`), typeExports);
  schemaNamesExport += `\n${key}='${key}',`;
}

schemaNamesExport += "\n}";
fs.writeFileSync(path.join(dir, `../src/schema-names-export.ts`), schemaNamesExport);

function schemaToKey(schema) {
  const mappingRegex = ".+/(.+).json$";
  return schema['$id'].match(mappingRegex)[1];
}