/**
 * Script to create optimized ES Module import files for each schema JSON file.
 * This script is run as part of the build process and at postinstall.
 */

import * as fs from "fs";
import glob from "glob";
import * as path from "path";
import * as url from "url";

import Ajv from "ajv";
import standaloneCode from "ajv/dist/standalone/index.js";

const versions = ["8.4", "8.5"];

const dir = path.dirname(url.fileURLToPath(import.meta.url));
fs.mkdirSync(path.join(dir, `../dist`), { recursive: true });

for (const version of versions) {
  const files = glob.sync(path.join(dir, `../../schema/${version}/*.json`));
  fs.mkdirSync(path.join(dir, `../dist/${version}`), { recursive: true });
  for (const file of files) {
    const schema = JSON.parse(fs.readFileSync(file, "utf-8"));

    // Ajv package is looking for 'http' in the schema definition URL and errors on 'https'
    const theSchemaUrl = schema["$schema"];
    schema["$schema"] = theSchemaUrl.replace("https", "http");

    // Remove properties unnecessary for validation to reduce bundle size
    for (let n in schema.properties) {
      delete schema.description;
      delete schema.properties[n].title;
      delete schema.properties[n].description;
      delete schema.properties[n].examples;
      delete schema.properties[n].fec_spec;
    }

    // And write the module definition and an accompanying typescript information (.d.ts) file
    const schemaModuleContent =
      "export const schema = " + JSON.stringify(schema);
    const baseFilename = path.basename(file).replace(".json", "");
    fs.writeFileSync(
      path.join(dir, `../dist/${version}/${baseFilename}.js`),
      schemaModuleContent
    );
    fs.writeFileSync(
      path.join(dir, `../dist/${version}/${baseFilename}.d.ts`),
      "export declare const schema: any;"
    );

    createValidatorForSchemaFile(schema, baseFilename, version);
  }
}

function createValidatorForSchemaFile(schema, baseFilename, version) {
  const schemaList = [];
  const schemaMapping = {};
  const key = baseFilename;

  schemaList.push(schema);
  schemaMapping[baseFilename] = schema.$id;

  const ajv = new Ajv({
    schemas: schemaList,
    code: {
      source: true,
      esm: true,
      optimize: true,
    },
    allErrors: true,
    strictSchema: false,
  });
  let moduleCode = removeInvalidCjsRequireStatements(
    standaloneCode(ajv, schemaMapping)
  );
  const typeExports = `export declare function ${key}(data: any, options: any): boolean;`;
  fs.writeFileSync(
    path.join(dir, `../dist/${version}/${key}.validator.js`),
    moduleCode
  );
  fs.writeFileSync(
    path.join(dir, `../dist/${version}/${key}.validator.d.ts`),
    typeExports
  );
}

// Due to this issue we have to hack at the generated js.
// standalone() is incorrectly leaving in 'require' statements.
// https://github.com/ajv-validator/ajv/issues/2209
function removeInvalidCjsRequireStatements(jsCode) {
  // inspired by this answer
  // https://github.com/ajv-validator/ajv/issues/2209#issuecomment-2577305143
  const preamble = '"use strict";';
  let importStatements = "";
  const requireRegex = /const (\S+)\s*=\s*require\((.+)\)\.(\S+);/g;
  const retval = jsCode
    .replace(requireRegex, (_match, p1, p2, p3) => {
      importStatements += `import { ${p3} as ${p1} } from ${p2};`;
      return "";
    })
    .replace(preamble, "");
  // Individual lib replacement to avoid webpack import issue
  // after several field validation cyles which we could not
  // determine why it was happening.  We may need more of these
  // in the future if our schemas add more require statements.
  importStatements = importStatements.replace(
    "ajv/dist/runtime/ucs2length",
    "../ucs2length.js"
  );
  return preamble + importStatements + retval;
}
