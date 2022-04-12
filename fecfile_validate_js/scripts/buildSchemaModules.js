/**
 * Script to create optimized ES Module import files for each schema JSON file.
 * This script is run as part of the build process and at postinstall.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as url from 'url';
import glob from 'glob';

const dir = path.dirname(url.fileURLToPath(import.meta.url));
const files = glob.sync(path.join(dir, '../../schema/*.json'));

for (const file of files) {
  const schema = JSON.parse(fs.readFileSync(file, 'utf-8'));

  // Ajv package is looking for 'http' in the schema definition URL and errors on 'https'
  const theSchemaUrl = schema['$schema'];
  schema['$schema'] = theSchemaUrl.replace('https', 'http');

  // Remove properties unnecessary for validation to reduce bundle size
  for (let n in schema.properties) {
    delete schema.description;
    delete schema.properties[n].title;
    delete schema.properties[n].description;
    delete schema.properties[n].examples;
    delete schema.properties[n].fec_spec;
  }

  // And write the module definition and an accompanying typescript information (.d.ts) file
  const schemaModuleContent = 'export const schema = ' + JSON.stringify(schema);
  const baseFilename = path.basename(file).replace('.json', '');
  fs.writeFileSync(path.join(dir, `../dist/${baseFilename}.js`), schemaModuleContent);
  fs.writeFileSync(path.join(dir, `../dist/${baseFilename}.d.ts`), 'export declare const schema: any;');
}
