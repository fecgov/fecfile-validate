import { assertEquals } from "https://deno.land/std/testing/asserts.ts";
import { validate } from "../dist/index.js";
import { schema } from "../dist/Contact_Individual.js";

const perfectForm: any = {
  type: "IND",
  last_name: "Smith",
  first_name: "John",
  middle_name: "W",
  prefix: "Dr",
  suffix: "Jr",
  street_1: "123 Main Street",
  street_2: "Test street 2",
  city: "Anytown",
  state: "WA",
  zip: "981110123",
  telephone: "+1 5555555555",
  employer: "XYZ Company",
  occupation: "QC Inspector",
  country: "United States",
};

Deno.test({
  name: "it should pass with perfect data",
  fn: async () => {
    const result = await validate(schema, perfectForm);
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should pass containing every allowed character",
  fn: async () => {
    const thisData = { ...perfectForm };
    const specialChars =
      " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
    thisData.last_name = specialChars.substring(0, 29);
    thisData.first_name = specialChars.substring(29, 48);
    thisData.middle_name = specialChars.substring(48, 67);
    thisData.street_1 = specialChars.substring(67);
    const result = await validate(schema, thisData);

    assertEquals(
      thisData.last_name + thisData.first_name + thisData.middle_name + thisData.street_1,
      specialChars
    );
    assertEquals(result, []);
  },
});

Deno.test({
  name: "it should fail containing disallowed character (tab) in last_name",
  fn: async () => {
    const thisData = { ...perfectForm };
    const disallowedChar = "\t";
    const specialChars =
      disallowedChar +
      " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~";
    thisData.last_name = specialChars.substring(0, 29);
    thisData.first_name = specialChars.substring(29, 48);
    thisData.middle_name = specialChars.substring(48, 67);
    thisData.street_1 = specialChars.substring(67);
    assertEquals(
      thisData.last_name + thisData.first_name + thisData.middle_name + thisData.street_1,
      specialChars
    );
    const result = await validate(schema, thisData);

    assertEquals(result[0].keyword, "pattern");
    assertEquals(result[0].message, 'must match pattern "^[ -~]{0,30}$"');
    assertEquals(result[0].params.pattern, "^[ -~]{0,30}$");
    assertEquals(result[0].path, "last_name");
  },
});
