import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { validate } from "../dist/index.js";
import { schema } from "../dist/COORDINATED_PARTY_EXPENDITURES.js";

const perfectSchedule: any = {
  form_type: "SF",
  filer_committee_id_number: "C00000000",
  transaction_type_identifier: "COORDINATED_PARTY_EXPENDITURE",
  transaction_id_number: "F123456",
  entity_type: "ORG",
  payee_organization_name: "Org Name",
  payee_street_1: "123 main street",
  payee_city: "City",
  payee_state: "DC",
  payee_zip: "20000",
  expenditure_date: "2022-09-15",
  expenditure_amount: 500,
  general_election_year: "2025",
  aggregate_general_elec_expended: 500,
  aggregation_group: "COORDINATED_PARTY_EXPENDITURES",
  expenditure_purpose_descrip: "a description",
  payee_committee_id_number: "C00000000",
  payee_candidate_id_number: "P00000000",
  payee_candidate_last_name: "Last",
  payee_candidate_first_name: "First",
  payee_candidate_office: "P",
};

Deno.test({
  name: "it should pass with perfect data",
  fn: async () => {
    const result = await validate(schema, perfectSchedule);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail if designating commiteee is selected and empty",
  fn: async () => {
    const thisData = { ...perfectSchedule };
    thisData.filer_designated_to_make_coordinated_expenditures = true;
    const result = await validate(schema, thisData);
    assertEquals(result[0].keyword, "required");
    assertEquals(result[0].path, "designating_committee_id_number");
    assertEquals(result[1].keyword, "required");
    assertEquals(result[1].path, "designating_committee_name");
    thisData.designating_committee_id_number = "C00000000";
    thisData.designating_committee_name = "Designating Committee";
    const result2 = await validate(schema, thisData);
    assertEquals(result2, []);
  },
});
Deno.test({
  name: "it should fail if subordinate commiteee is selected and empty",
  fn: async () => {
    const thisData = { ...perfectSchedule };
    thisData.subordinate_committee_id_number = "C00000000";
    const result = await validate(schema, thisData);
    assertEquals(result[0].keyword, "required");
    assertEquals(result[0].path, "subordinate_committee_name");
    assertEquals(result[1].keyword, "required");
    assertEquals(result[1].path, "subordinate_street_1");
    assertEquals(result[2].keyword, "required");
    assertEquals(result[2].path, "subordinate_city");
    assertEquals(result[3].keyword, "required");
    assertEquals(result[3].path, "subordinate_state");
    assertEquals(result[4].keyword, "required");
    assertEquals(result[4].path, "subordinate_zip");
    assertEquals(result[5].keyword, "if");
    thisData.subordinate_committee_id_number = "C00000000";
    thisData.subordinate_street_1 = "123 main street";
    thisData.subordinate_city = "City";
    thisData.subordinate_state = "DC";
    thisData.subordinate_zip = "20000";
    thisData.subordinate_committee_name = "Subordinate Committee";
    const result2 = await validate(schema, thisData);
    assertEquals(result2, []);
  },
});
