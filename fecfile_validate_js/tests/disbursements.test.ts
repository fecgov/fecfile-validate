import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { validate } from "../dist/index.js";
import { schema } from "../dist/DISBURSEMENTS.js";

const perfectForm: any = {
  report_type: "F3X",
  form_type: "SB21B",
  filer_committee_id_number: "C00123456",
  transaction_type_identifier: "OPERATING_EXPENDITURE",
  transaction_id: "A12345678",
  back_reference_tran_id_number: null,
  back_reference_sched_name: null,
  entity_type: "IND",
  payee_organization_name: null,
  payee_last_name: "Smith",
  payee_first_name: "Bob",
  payee_middle_name: null,
  payee_prefix: null,
  payee_suffix: null,
  payee_street_1: "123 main street",
  payee_street_2: "",
  payee_city: "Best Town",
  payee_state: "DC",
  payee_zip: "20000",
  expenditure_date: "2022-09-15",
  expenditure_amount: 500,
  aggregate_amount: 0,
  aggregation_group: "GENERAL_DISBURSEMENT",
  expenditure_purpose_descrip: "a description",
  memo_code: false,
  memo_text_description: "memo text description",
};

Deno.test({
  name: "it should pass with perfect data",
  fn: async () => {
    const result = await validate(schema, perfectForm);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail if VOID transaction type and expenditure amount positive",
  fn: async () => {
    const thisData = { ...perfectForm };
    thisData.transaction_type_identifier = "OPERATING_EXPENDITURE_VOID";
    const result = await validate(schema, thisData);
    assertEquals(result[0].keyword, "exclusiveMaximum");
    assertEquals(result[0].path, "expenditure_amount");
    assertEquals(result[0].keyword, "exclusiveMaximum");
  },
});

Deno.test({
  name: "it should pass if VOID transaction type and expenditure amout negative",
  fn: async () => {
    const thisData = { ...perfectForm };
    thisData.transaction_type_identifier = "OPERATING_EXPENDITURE_VOID";
    thisData.expenditure_amount = -55.01;
    const result = await validate(schema, thisData);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail if VOID transaction type and expenditure is zero",
  fn: async () => {
    const thisData = { ...perfectForm };
    thisData.transaction_type_identifier = "OPERATING_EXPENDITURE_VOID";
    thisData.expenditure_amount = -0.0;
    const result = await validate(schema, thisData);
    assertEquals(result[0].keyword, "exclusiveMaximum");
    assertEquals(result[0].path, "expenditure_amount");
    assertEquals(result[0].keyword, "exclusiveMaximum");
  },
});
