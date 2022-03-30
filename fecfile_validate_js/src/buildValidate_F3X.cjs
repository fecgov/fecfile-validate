const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const standaloneCode = require('ajv/dist/standalone').default;

let schema_F3X = require('../../schema/F3X.json');

const theSchemaUrl = schema_F3X['$schema'];
schema_F3X['$schema'] = theSchemaUrl.replace('https', 'http');

const error_fec_recommended = {
  message: ({ params: { missingProperty } }) => `must have required property '${missingProperty}'`,
  params: ({ params: { missingProperty } }) => `{missingProperty: ${missingProperty}}`,
};

const keyword_fec_recommended = {
  keyword: 'fec_recommended',
  type: 'object',
  schemaType: 'array',
  // $data: true,
  error_fec_recommended,
  // code(var1) {
  // console.log('fec_recommended: var1: ', var1);
  // const {gen, schema, schemaCode, data, $data, it} = cxt
  // const {opts} = it
  // if (!$data && schema.length === 0) return
  // const useLoop = schema.length >= opts.loopRequired
  // if (it.allErrors) allErrorsMode()
  // else exitOnErrorMode()

  // if (opts.strictRequired) {
  //   const props = cxt.parentSchema.properties
  //   const {definedProperties} = cxt.it
  //   for (const requiredKey of schema) {
  //     if (props?.[requiredKey] === undefined && !definedProperties.has(requiredKey)) {
  //       const schemaPath = it.schemaEnv.baseId + it.errSchemaPath
  //       const msg = `required property "${requiredKey}" is not defined at "${schemaPath}" (strictRequired)`
  //       checkStrictMode(it, msg, it.opts.strictRequired)
  //     }
  //   }
  // }

  // function allErrorsMode(): void {
  //   if (useLoop || $data) {
  //     cxt.block$data(nil, loopAllRequired)
  //   } else {
  //     for (const prop of schema) {
  //       checkReportMissingProp(cxt, prop)
  //     }
  //   }
  // }

  // function exitOnErrorMode(): void {
  //   const missing = gen.let("missing")
  //   if (useLoop || $data) {
  //     const valid = gen.let("valid", true)
  //     cxt.block$data(valid, () => loopUntilMissing(missing, valid))
  //     cxt.ok(valid)
  //   } else {
  //     gen.if(checkMissingProp(cxt, schema, missing))
  //     reportMissingProp(cxt, missing)
  //     gen.else()
  //   }
  // }

  // function loopAllRequired(): void {
  //   gen.forOf("prop", schemaCode as Code, (prop) => {
  //     cxt.setParams({missingProperty: prop})
  //     gen.if(noPropertyInData(gen, data, prop, opts.ownProperties), () => cxt.error())
  //   })
  // }

  // function loopUntilMissing(missing: Name, valid: Name): void {
  //   cxt.setParams({missingProperty: missing})
  //   gen.forOf(
  //     missing,
  //     schemaCode as Code,
  //     () => {
  //       gen.assign(valid, propertyInData(gen, data, missing, opts.ownProperties))
  //       gen.if(not(valid), () => {
  //         cxt.error()
  //         gen.break()
  //       })
  //     },
  //     nil
  //   )
  // }
  // }
};

// Remove the fec_spec from every field
for (var n in schema_F3X.properties) {
  delete schema_F3X.properties[n].fec_spec;
}

// Create the ajv instance
const ajv = new Ajv({
  code: { source: true },
});

// Allow the 'version' root keyword
ajv.addKeyword({
  keyword: 'version',
});

// Define the keyword fec_recommended
ajv.addKeyword(keyword_fec_recommended);

// Compile the schema
const validate = ajv.compile(schema_F3X);

// Make it into standalone code
const moduleCode = standaloneCode(ajv, validate);

// And write the module code to file
fs.writeFileSync(path.join(__dirname, './validate-F3X.js'), moduleCode);
