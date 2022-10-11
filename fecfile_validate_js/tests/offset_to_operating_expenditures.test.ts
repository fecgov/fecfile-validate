import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { validate } from "../dist/index.js";
import { schema } from "../dist/OFFSET_TO_OPERATING_EXPENDITURES.js";

const perfectForm: any = {
  form_type: "SA15",
  filer_committee_id_number: "C00123456",
  transaction_type_identifier: "OFFSET_TO_OPERATING_EXPENDITURES",
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
  aggregation_group: "LINE_15",
  contribution_purpose_descrip: "a description",
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
  name: "it should fail if contribution_amount is null",
  fn: () => {
    const thisData = { ...perfectForm };
    thisData.contribution_amount = null;
    const result = validate(schema, thisData);
    assertEquals(result[0].keyword, "type");
    assertEquals(result[0].path, "contribution_amount");
    assertEquals(result[0].params.type, "number");
  },
});

Deno.test({
  name: "it should be contributor_organization_name is required for ORG and contributor_first_name not required",
  fn: () => {
    const thisData = { ...perfectForm };
    thisData.entity_type = "ORG";
    thisData.contributor_first_name = null;
    const result = validate(schema, thisData);
    assertEquals(result[0].keyword, "type");
    assertEquals(result[0].path, "contributor_organization_name");
    assertEquals(result[0].params.type, "string");
    assertEquals(result[1].keyword, "if");
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
