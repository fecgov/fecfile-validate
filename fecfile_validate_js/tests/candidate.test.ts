import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { validate } from "../dist/index.js";
import { schema as candidateContactSchema } from "../dist/8.5/Contact_Candidate.js";

const data: any = {
  type: "CAN",
  candidate_id: "H0AZ12345",
  committee_id: "C00601211",
  name: "Gilbert Smith",
  last_name: "Smith",
  first_name: "Gilbert",
  middle_name: null,
  prefix: null,
  suffix: null,
  street_1: "602 Tlumacki St",
  street_2: null,
  city: "Mclean City",
  state: "VA",
  zip: "22204",
  employer: null,
  occupation: null,
  candidate_office: "P",
  candidate_state: null,
  candidate_district: null,
  telephone: "+1 3043892120",
  country: "US",
};

Deno.test({
  name: "it should pass with perfect data",
  fn: async () => {
    const result = await validate(candidateContactSchema, data);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail as S candidate office missing",
  fn: async () => {
    const testData = { ...data };
    delete testData.candidate_office;
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].keyword, "required");
    assertEquals(result[0].path, "candidate_office");
    assertEquals(
      result[0].message,
      "must have required property 'candidate_office'"
    );
  },
});

Deno.test({
  name: "it should fail as S candidate office and null for candidate_state",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "S";
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].path, "candidate_state");
    assertEquals(result[0].message, "must be string");
  },
});

Deno.test({
  name: "it should fail as S candidate office and candidate_state missing",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "S";
    delete testData.candidate_state;
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].keyword, "required");
    assertEquals(result[0].path, "candidate_state");
    assertEquals(
      result[0].message,
      "must have required property 'candidate_state'"
    );
  },
});

Deno.test({
  name: "it should fail with for candidate office S with an invalid candidate state format",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "S";
    testData.candidate_state = "M1";
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].path, "candidate_state");
    assertEquals(result[0].message, 'must match pattern "^[A-Z]{2}$"');
  },
});

Deno.test({
  name: "it should pass with for candidate office S with a candidate state",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "S";
    testData.candidate_state = "VA";
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail as H candidate office and null for candidate_state",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "H";
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].path, "candidate_state");
    assertEquals(result[0].message, "must be string");
  },
});

Deno.test({
  name: "it should fail as H candidate office and candidate_state missing",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "H";
    delete testData.candidate_state;
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].keyword, "required");
    assertEquals(result[0].path, "candidate_state");
    assertEquals(
      result[0].message,
      "must have required property 'candidate_state'"
    );
  },
});

Deno.test({
  name: "it should fail as H candidate office and null for candidate_district",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "H";
    testData.candidate_state = "MD";
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].path, "candidate_district");
    assertEquals(result[0].message, "must be string");
  },
});

Deno.test({
  name: "it should fail as H candidate office and candidate_district missing",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "H";
    testData.candidate_state = "VA";
    delete testData.candidate_district;
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result[0].keyword, "required");
    assertEquals(result[0].path, "candidate_district");
    assertEquals(
      result[0].message,
      "must have required property 'candidate_district'"
    );
  },
});

Deno.test({
  name: "it should pass with for candidate office H with a candidate state and candidate district",
  fn: async () => {
    const testData = { ...data };
    testData.candidate_office = "H";
    testData.candidate_state = "VA";
    testData.candidate_district = "01";
    const result = await validate(candidateContactSchema, testData);
    assertEquals(result, []);
  },
});
