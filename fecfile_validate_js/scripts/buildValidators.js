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

  const schemaList = [];
  const schemaMapping = {}; 

  schemaList.push(schema);
  schemaMapping[key] = schema.$id;

  const ajv = new Ajv({schemas: schemaList, code: {source: true, esm: true}, allErrors: true, strictSchema: false});
  let moduleCode = removeInvalidCjsRequireStatements(standaloneCode(ajv, schemaMapping));
  const typeExports = `export declare function ${key}(data: any, options: any): boolean;`
  //const ajv = new Ajv({ code: { source: true, esm: true } });
  //const validate = ajv.compile(schema);
  //const moduleCode = removeInvalidCjsRequireStatements(standaloneCode(ajv, validate));
  fs.writeFileSync(path.join(dir, `../dist/${key}_VALIDATOR.js`), moduleCode);
  fs.writeFileSync(path.join(dir, `../dist/${key}_VALIDATOR.d.ts`), typeExports);
  schemaNamesExport += `\n${key}='${key}',`;
}

//const ajv = new Ajv({schemas: schemaList, code: {source: true, esm: true}});
//let moduleCode = standaloneCode(ajv, schemaMapping);

schemaNamesExport += "\n}";
fs.writeFileSync(path.join(dir, `../src/schema-names-export.ts`), schemaNamesExport);

function schemaToKey(schema) {
  const mappingRegex = ".+/(.+).json$";
  return schema['$id'].match(mappingRegex)[1];
}

// Due to this issue we have to hack at the generated js.
// standalone() is incorrectly leaving in 'require' statements.
// https://github.com/ajv-validator/ajv/issues/2209
function removeInvalidCjsRequireStatements(jsCode) {
  // inspired by this answer
  // https://github.com/ajv-validator/ajv/issues/2209#issuecomment-2577305143
  const preamble = '"use strict";';
  const requireRegex = /const (\S+)\s*=\s*require\((.+)\)\.(\S+);/g;
  let retval = jsCode.replace(requireRegex, (_match, p1, p2, p3) => {
    return "";
  })
  .replace(preamble, "");
  //const importStatements = 'import func2 from "ajv/dist/runtime/ucs2length";';
  const importStatements = 'import func2 from "./ucs2length";';
  return preamble + importStatements + retval;
}