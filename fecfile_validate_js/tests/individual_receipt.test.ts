import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { validate } from "../dist/index.js";
import { schema } from "../dist/INDIVIDUAL_RECEIPT.js";

const perfectForm: any = {
  form_type: "SA11AI",
  filer_committee_id_number: "C00123456",
  transaction_type_identifier: "INDIVIDUAL_RECEIPT",
  transaction_id: "A12345678",
  back_reference_tran_id_number: null,
  back_reference_sched_name: null,
  entity_type: "IND",
  contributor_organization_name: null,
  contributor_last_name: "Smith",
  contributor_first_name: "Bob",
  contributor_middle_name: null,
  contributor_prefix: null,
  contributor_suffix: null,
  contributor_street_1: "123 main street",
  contributor_street_2: "",
  contributor_city: "Best Town",
  contributor_state: "DC",
  contributor_zip: "20000",
  contribution_date: "2022-09-15",
  contribution_amount: 500,
  contribution_aggregate: 0,
  contribution_purpose_descrip: "a description",
  contributor_employer: "employer",
  contributor_occupation: "occupation",
  memo_code: false,
  memo_text_description: "memo text description",
};

Deno.test({
  name: "it should pass with perfect data",
  fn: () => {
    const result = validate(schema, perfectForm);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail if contribution_aggregate > 200 and missing contribution_employer",
  fn: () => {
    const thisData = { ...perfectForm };
    thisData.contribution_aggregate = 200.01;
    thisData.contributor_employer = null;
    const result = validate(schema, thisData);
    assertEquals(result[0].keyword, "type");
    assertEquals(result[0].path, "contributor_employer");
    assertEquals(result[0].params.type, "string");
    assertEquals(result[1].keyword, "if");
  },
});

Deno.test({
  name: "it should pass if contribution_aggregate > 200 and have contribution_employer",
  fn: () => {
    const thisData = { ...perfectForm };
    thisData.contribution_aggregate = 200.01;
    const result = validate(schema, thisData);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should pass if contribution_aggregate =< 200 and missing contribution_employer",
  fn: () => {
    const thisData = { ...perfectForm };
    thisData.contribution_aggregate = 200;
    thisData.contributor_employer = null;
    const result = validate(schema, thisData);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should pass if contribution_amount == 999999999.99",
  fn: ()=>{
    const thisData = {...perfectForm};
    thisData.contribution_amount = 999999999.99;
    const result = validate(schema, thisData);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail if contribution_amount > 999999999.99",
  fn: ()=>{
    const thisData = {...perfectForm};
    thisData.contribution_amount = 1000000000;
    const result = validate(schema, thisData);
    const failure = (result.length > 0);
    assertEquals(failure, true);
  },
});
