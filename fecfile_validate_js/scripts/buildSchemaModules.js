/**
 * Script to create optimized ES Module import files for each schema JSON file.
 * This script is run as part of the build process and at postinstall.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as url from 'url';
import glob from 'glob';
import Ajv from 'ajv';
import standaloneCode from 'ajv/dist/standalone/index.js';

const dir = path.dirname(url.fileURLToPath(import.meta.url));
const files = glob.sync(path.join(dir, '../../schema/*.json'));

const schemaList = [];
const schemaMapping = {};
let typeExports = '';
for (const file of files) {
  const schema = JSON.parse(fs.readFileSync(file, 'utf-8'));

  // Ajv package is looking for 'http' in the schema definition URL and errors on 'https'
  const theSchemaUrl = schema['$schema'];
  schema['$schema'] = theSchemaUrl.replace('https', 'http');

  // Remove properties unnecessary for validation to reduce bundle size
  for (let n in schema.properties) {
    delete schema.description;
    delete schema.version;
    delete schema.fec_recommended;
    delete schema.properties[n].title;
    delete schema.properties[n].description;
    delete schema.properties[n].examples;
    delete schema.properties[n].fec_spec;
  }

  schemaList.push(schema);
  const key = schemaToKey(schema);
  schemaMapping[key] = schema['$id'];
  // And write the module definition and an accompanying typescript information (.d.ts) file
  //const schemaModuleContent = 'export const schema = ' + JSON.stringify(schema);
  //const baseFilename = path.basename(file).replace('.json', '');
  //fs.writeFileSync(path.join(dir, `../dist/${baseFilename}.js`), schemaModuleContent);
  //fs.writeFileSync(path.join(dir, `../dist/${baseFilename}.d.ts`), 'export declare const schema: any;');
  typeExports += `export declare function ${key}(data: any, options: any): boolean;`
}
//console.log('==============' + JSON.stringify(schemaList[0]));

const ajv = new Ajv({schemas: schemaList, code: {source: true, esm: true}})
let moduleCode = standaloneCode(ajv, schemaMapping);
fs.mkdirSync(path.join(dir, `../dist`), { recursive: true });
fs.writeFileSync(path.join(dir, `../dist/validate-esm.mjs`), moduleCode);
fs.writeFileSync(path.join(dir, `../dist/validate-esm.d.mts`), typeExports);

function schemaToKey(schema) {
  const mappingRegex = ".+/(.+).json$";
  return schema['$id'].match(mappingRegex)[1];
}