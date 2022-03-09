import Ajv from 'ajv';
const ajv = new Ajv({allErrors: true, $data: true});

import * as draft7MetaSchema from "ajv/dist/refs/json-schema-draft-07.json"

import * as schema_F3X from './../../schema/F3X.json';
// import { readdir, readFileSync } from 'fs';
// import { extname, parse as parsePath } from 'path';

// const pathToSchemaFiles = './../../../schema/';


// ajv.addSchema(schema_F3X, 'F3X');

// const form_F3X {
//   'form_type': string,
//   'filer_committee_id_number': string,
//   'committee_name': string,
//   'change_of_address': boolean,
//   'street_1': string,
//   'street_2': string,
//   'city': string,
//   'state': string,
//   'zip': string,
//   'report_code': string,
//   'election_code': string,
//   'date_of_election': string,
//   'state_of_election': string,
//   'coverage_from_date': string,
//   'coverage_through_date': string,
//   'qualified_committee': boolean,
//   'treasurer_last_name': string,
//   'treasurer_first_name': string,
//   'treasurer_middle_name': string,
//   'treasurer_prefix': string,
//   'treasurer_suffix': string,
//   'date_signed': string,
//   'L6b_cash_on_hand_beginning_period': number
// }



const testData = {
  "form_type": "F3XA",
  "filer_committee_id_number": "C00123456",
  "committee_name": "Foes of Pat"
}
const testSchema = {
  type: "object",
  required: [
    "form_type",
    "filer_committee_id_number",
    "treasurer_last_name",
    "treasurer_first_name",
    "date_signed"
  ],
  properties: {
    form_type: {
      title: "FORM TYPE",
      description: "",
      type: "string",
      enum: ["F3XN", "F3XA", "F3XT"],
      examples: ["F3XN"],
    },
    "filer_committee_id_number": {
      "title": "FILER COMMITTEE ID NUMBER",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 9,
      "pattern": "^[ A-Za-z0-9]{0,9}$",
      "examples": ["C00123456"]
    },
    "committee_name": {
      "title": "COMMITTEE NAME",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 200,
      "pattern": "^[ A-Za-z0-9]{0,200}$",
      "examples": ["Foes of Pat"]
    },
    "change_of_address": {
      "title": "CHANGE OF ADDRESS",
      "description": "",
      "type": "boolean",
      "examples": ["X"]
    },
    "street_1": {
      "title": "STREET  1",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 34,
      "pattern": "^[ A-Za-z0-9]{0,34}$",
      "examples": ["125 Sycamore St"]
    },
    "street_2": {
      "title": "STREET  2",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 34,
      "pattern": "^[ A-Za-z0-9]{0,34}$"
    },
    "city": {
      "title": "CITY",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 30,
      "pattern": "^[ A-Za-z0-9]{0,30}$",
      "examples": ["Anytown"]
    },
    "state": {
      "title": "STATE",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 2,
      "pattern": "^[ A-Za-z0-9]{0,2}$",
      "examples": ["FL"]
    },
    "zip": {
      "title": "ZIP",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 9,
      "pattern": "^[ A-Za-z0-9]{0,9}$",
      "examples": [33034]
    },
    "report_code": {
      "title": "REPORT CODE",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 3,
      "pattern": "^[ A-Za-z0-9]{0,3}$",
      "examples": ["12P"]
    },
    "election_code": {
      "title": "ELECTION CODE",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 5,
      "pattern": "^[ A-Za-z0-9]{0,5}$",
      "examples": ["P2012"]
    },
    "date_of_election": {
      "title": "DATE OF ELECTION",
      "description": "",
      "type": "string",
      "minLength": 8,
      "maxLength": 8,
      "pattern": "^\\d{8}$",
      "examples": [20120715]
    },
    "state_of_election": {
      "title": "STATE OF ELECTION",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 2,
      "pattern": "^[ A-Za-z0-9]{0,2}$",
      "examples": ["FL"]
    },
    "coverage_from_date": {
      "title": "COVERAGE FROM DATE",
      "description": "",
      "type": "string",
      "minLength": 8,
      "maxLength": 8,
      "pattern": "^\\d{8}$"
    },
    "coverage_through_date": {
      "title": "COVERAGE THROUGH DATE",
      "description": "",
      "type": "string",
      "minLength": 8,
      "maxLength": 8,
      "pattern": "^\\d{8}$"
    },
    "qualified_committee": {
      "title": "QUALIFIED COMMITTEE",
      "description": "",
      "type": "boolean",
      "examples": ["X"]
    },
    "treasurer_last_name": {
      "title": "TREASURER LAST NAME",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 30,
      "pattern": "^[ A-Za-z0-9]{0,30}$",
      "examples": ["Smith"]
    },
    "treasurer_first_name": {
      "title": "TREASURER FIRST NAME",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 20,
      "pattern": "^[ A-Za-z0-9]{0,20}$",
      "examples": ["Patrick"]
    },
    "treasurer_middle_name": {
      "title": "TREASURER MIDDLE NAME",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 20,
      "pattern": "^[ A-Za-z0-9]{0,20}$",
      "examples": ["Thomas"]
    },
    "treasurer_prefix": {
      "title": "TREASURER PREFIX",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 10,
      "pattern": "^[ A-Za-z0-9]{0,10}$",
      "examples": ["Mr."]
    },
    "treasurer_suffix": {
      "title": "TREASURER SUFFIX",
      "description": "",
      "type": "string",
      "minLength": 0,
      "maxLength": 10,
      "pattern": "^[ A-Za-z0-9]{0,10}$",
      "examples": ["Jr."]
    },
    "date_signed": {
      "title": "DATE SIGNED",
      "description": "",
      "type": "string",
      "minLength": 8,
      "maxLength": 8,
      "pattern": "^\\d{8}$",
      "examples": [20040729]
    },
    "L6b_cash_on_hand_beginning_period": {
      "title": "6(b) Cash on Hand beginning",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999,
      "examples": [1123123.45]
    },
    "L6c_total_receipts_period": {
      "title": "6(c) Total Receipts",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L6d_subtotal_period": {
      "title": "6(d) Subtotal",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L7_total_disbursements_period": {
      "title": "7. Total Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L8_cash_on_hand_at_close_period": {
      "title": "8. Cash on Hand at Close",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L9_debts_to_period": {
      "title": "9. Debts to",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L10_debts_by_period": {
      "title": "10. Debts by",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11ai_itemized_period": {
      "title": "11(a)i  Itemized",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11aii_unitemized_period": {
      "title": "11(a)ii  Unitemized",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11aiii_total_period": {
      "title": "11(a)iii Total",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11b_political_party_committees_period": {
      "title": "11(b) Political Party Committees",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11c_other_political_committees_pacs_period": {
      "title": "11(c) Other Political Committees (PACs)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11d_total_contributions_period": {
      "title": "11(d) Total Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L12_transfers_from_affiliated_other_party_cmtes_period": {
      "title": "12. Transfers from Affiliated/Other Party Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L13_all_loans_received_period": {
      "title": "13. All Loans Received",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L14_loan_repayments_received_period": {
      "title": "14. Loan Repayments Received",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L15_offsets_to_operating_expenditures_refunds_period": {
      "title": "15. Offsets to Operating Expenditures (refunds)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L16_refunds_of_federal_contributions_period": {
      "title": "16. Refunds of Federal Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L17_other_federal_receipts_dividends_period": {
      "title": "17. Other Federal Receipts (dividends)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L18a_transfers_from_nonfederal_account_h3_period": {
      "title": "18(a) Transfers from Nonfederal Account (H3)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L18b_transfers_from_nonfederal_levin_h5_period": {
      "title": "18(b) Transfers from Non-Federal (Levin - H5)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L18c_total_nonfederal_transfers_18a_18b_period": {
      "title": "18(c) Total Non-Federal Transfers (18a+18b)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L19_total_receipts_period": {
      "title": "19. Total Receipts",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L20_total_federal_receipts_period": {
      "title": "20. Total Federal Receipts",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21ai_federal_share_period": {
      "title": "21(a)i  Federal Share",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21aii_nonfederal_share_period": {
      "title": "21(a)ii  Non-Federal Share",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21b_other_federal_operating_expenditures_period": {
      "title": "21(b)  Other Federal Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21c_total_operating_expenditures_period": {
      "title": "21(c)  Total Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L22_transfers_to_affiliated_other_party_cmtes_period": {
      "title": "22. Transfers to Affiliated/Other Party Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L23_contributions_to_federal_candidates_cmtes_period": {
      "title": "23. Contributions to Federal Candidates/Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L24_independent_expenditures_period": {
      "title": "24. Independent Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L25_coordinated_expend_made_by_party_cmtes_period": {
      "title": "25. Coordinated Expend made by Party Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L26_loan_repayments_period": {
      "title": "26. Loan Repayments",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L27_loans_made_period": {
      "title": "27. Loans Made",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28a_individuals_persons_period": {
      "title": "28(a) Individuals/Persons",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28b_political_party_committees_period": {
      "title": "28(b) Political Party Committees",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28c_other_political_committees_period": {
      "title": "28(c) Other Political Committees",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28d_total_contributions_refunds_period": {
      "title": "28(d) Total Contributions Refunds",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L29_other_disbursements_period": {
      "title": "29. Other Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30ai_shared_federal_activity_h6_fed_share_period": {
      "title": "30(a)i  Shared Federal Activity (H6) Fed Share",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30aii_shared_federal_activity_h6_nonfed_period": {
      "title": "30(a)ii Shared Federal Activity (H6) Non-Fed",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30b_nonallocable_fed_election_activity_period": {
      "title": "30(b) Non-Allocable 100% Fed Election Activity",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30c_total_federal_election_activity_period": {
      "title": "30(c) Total Federal Election Activity",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L31_total_disbursements_period": {
      "title": "31. Total Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L32_total_federal_disbursements_period": {
      "title": "32. Total Federal Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L33_total_contributions_period": {
      "title": "33. Total Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L34_total_contribution_refunds_period": {
      "title": "34. Total Contribution Refunds",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L35_net_contributions_period": {
      "title": "35. Net Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L36_total_federal_operating_expenditures_period": {
      "title": "36. Total Federal Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L37_offsets_to_operating_expenditures_period": {
      "title": "37. Offsets to Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L38_net_operating_expenditures_period": {
      "title": "38. Net Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L6a_cash_on_hand_jan_1_ytd": {
      "title": "6(a) Cash on Hand Jan 1, 19",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999,
      "examples": [3123123.45]
    },
    "L6a_year_for_above_ytd": {
      "title": "Year for Above",
      "description": "",
      "type": "string",
      "minLength": 4,
      "maxLength": 4,
      "pattern": "^\\d{4}$",
      "examples": [2012]
    },
    "L6c_total_receipts_ytd": {
      "title": "6(c) Total Receipts",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L6d_subtotal_ytd": {
      "title": "6(d) Subtotal",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L7_total_disbursements_ytd": {
      "title": "7. Total disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L8_cash_on_hand_close_ytd": {
      "title": "8. Cash on Hand Close",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11ai_itemized_ytd": {
      "title": "11(a)i  Itemized",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11aii_unitemized_ytd": {
      "title": "11(a)ii  Unitemized",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11aiii_total_ytd": {
      "title": "11(a)iii Total",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11b_political_party_committees_ytd": {
      "title": "11(b) Political Party committees",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11c_other_political_committees_pacs_ytd": {
      "title": "11(c) Other Political Committees  (PACs)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L11d_total_contributions_ytd": {
      "title": "11(d) Total Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L12_transfers_from_affiliated_other_party_cmtes_ytd": {
      "title": "12. Transfers from Affiliated/Other Party Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L13_all_loans_received_ytd": {
      "title": "13. All Loans Received",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L14_loan_repayments_received_ytd": {
      "title": "14. Loan Repayments Received",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L15_offsets_to_operating_expenditures_refunds_ytd": {
      "title": "15. Offsets to Operating Expenditures (refunds)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L16_refunds_of_federal_contributions_ytd": {
      "title": "16. Refunds of Federal Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L17_other_federal_receipts_dividends_ytd": {
      "title": "17. Other Federal Receipts (dividends)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L18a_transfers_from_nonfederal_account_h3_ytd": {
      "title": "18(a) Transfers from Nonfederal Account (H3)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L18b_transfers_from_nonfederal_levin_h5_ytd": {
      "title": "18(b) Transfers from Non-Federal (Levin - H5)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L18c_total_nonfederal_transfers_18a_18b_ytd": {
      "title": "18(c) Total Non-Federal Transfers (18a+18b)",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L19_total_receipts_ytd": {
      "title": "19. Total Receipts",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L20_total_federal_receipts_ytd": {
      "title": "20. Total Federal Receipts",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21ai_federal_share_ytd": {
      "title": "21(a)i Federal Share",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21aii_nonfederal_share_ytd": {
      "title": "21(a)ii Non-Federal Share",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21b_other_federal_operating_expenditures_ytd": {
      "title": "21(b) Other Federal Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L21c_total_operating_expenditures_ytd": {
      "title": "21(c) Total operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L22_transfers_to_affiliated_other_party_cmtes_ytd": {
      "title": "22. Transfers to Affiliated/Other Party Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L23_contributions_to_federal_candidates_cmtes_ytd": {
      "title": "23. Contributions to Federal Candidates/Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L24_independent_expenditures_ytd": {
      "title": "24. Independent Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L25_coordinated_expend_made_by_party_cmtes_ytd": {
      "title": "25. Coordinated Expend made by Party Cmtes",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L26_loan_repayments_made_ytd": {
      "title": "26. Loan Repayments Made",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L27_loans_made_ytd": {
      "title": "27. Loans Made",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28a_individuals_persons_ytd": {
      "title": "28(a) Individuals/Persons",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28b_political_party_committees_ytd": {
      "title": "28(b) Political Party Committees",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28c_other_political_committees_ytd": {
      "title": "28(c) Other Political  Committees",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L28d_total_contributions_refunds_ytd": {
      "title": "28(d) Total contributions Refunds",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L29_other_disbursements_ytd": {
      "title": "29. Other Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30ai_shared_federal_activity_h6_fed_share_ytd": {
      "title": "30(a)i  Shared Federal Activity (H6) Fed Share",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30aii_shared_federal_activity_h6_nonfed_ytd": {
      "title": "30(a)ii Shared Federal Activity (H6) Non-Fed",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30b_nonallocable_fed_election_activity_ytd": {
      "title": "30(b) Non-Allocable 100% Fed Election Activity",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L30c_total_federal_election_activity_ytd": {
      "title": "30(c) Total Federal Election Activity",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L31_total_disbursements_ytd": {
      "title": "31. Total Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L32_total_federal_disbursements_ytd": {
      "title": "32. Total Federal Disbursements",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L33_total_contributions_ytd": {
      "title": "33. Total Contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L34_total_contribution_refunds_ytd": {
      "title": "34. Total Contribution Refunds",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L35_net_contributions_ytd": {
      "title": "35. Net contributions",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L36_total_federal_operating_expenditures_ytd": {
      "title": "36. Total Federal Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L37_offsets_to_operating_expenditures_ytd": {
      "title": "37. Offsets to Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    },
    "L38_net_operating_expenditures_ytd": {
      "title": "38. Net Operating Expenditures",
      "description": "",
      "type": "number",
      "minimum": 0,
      "maximum": 999999999999
    }
  },
  "additionalProperties": false
}

let schemas: {[k: string]: any} = {};



// readdir(pathToSchemaFiles, (err, files) => {
//   files.forEach(file => {
//     const filePathStr = `${pathToSchemaFiles}${file}`;
//     const filePath = parsePath(filePathStr);

//     console.log('extname: ', extname(file));

//     if (filePath.ext == '.json') {
//       // It's a json file so let's add it to schemas
//       readFile(filePathStr, (err, data) => {
//         if (err) throw err;
//         else {
//           console.log('err, data: ', err, data);
//         }
//       });
//     };
//   });
// });

/**
 * Return form schema as JSON object
 * @param {string} schemaID
 * @returns 
 */
async function getSchema(schemaID: string = 'F3X') {
  console.log('getSchema(schemaID): ', schemaID);
  
  // let rawData = require(schemaPath);
  // // readFileSync(schemaPath);
  // let json = JSON.parse(rawData);
  // schemas[schemaID] = json;
  // console.log('schemas: ', schemas);
  
  // console.log('schemaFile: ', schemaFile);

  // readdir(pathToSchemaFiles, (err, files) => {
  //   files.forEach(file => {
  //     console.log(file);
  //   });
  // });
  // with open(
  //     os.path.join(os.path.dirname(__file__), '../schema/F3X.json')
  // ) as fp:
  //   formSchema = json.load(fp)
  // return form_schema
}

/**
 * Wrapper function around jsonschema validator
 * @param {string} schemaId
 * @param {object} data
 * @returns {object} ajv output of error and warnings ex: 
 * {'errors': [{ 'path': 'property_name', 'message': 'message to user describing error' }, …], 'warnings': [] }
 */
 function validate(schemaId: string = 'F3X', data: object = testData) {
  console.log('validate()');
  // getSchema('f3x');

  // const serialize = compileSerializer(testSchema);
  
  // ajv.addMetaSchema(draft7MetaSchema);

  const compiledFunc = ajv.compile(testSchema);
  
  console.log('hasBeenCompiled: ');

  const validated = compiledFunc(testData);
  if (!validated) console.log('ERRORS: ', validated);
  else console.log('VALID!');

  
  // if (valid) {
  //   console.log('woo hoo!!');
  // } else {
  //   console.log('NOT VALID:');
  //   console.log(ajv.errors);
  // }

  // let formSchema = getSchema();
  // let validator = ajv(formSchema);
  // let errors = validator.iter_errors(formData);
  // let toReturn = errors.sort((val1, val2) => {
  //   const a = val1.toUpperCase();
  //   const b = val2.toUpperCase();
  //   if (a < b) return -1;
  //   else if (a > b) return 1;
  //   else return 0;
  // })
  // return toReturn;
 }

 /**
 * Wrapper function around jsonschema validator
 * @param {string} schemaId
 * @param {string} key
 * @param {string|number} value
 * @returns {string|null} error message string, else null if valid
 */
function validateItem(schemaId: string, key: string, value: (string|number)) {
  console.log('validateItem()');
  // getSchema('f3x');
  // let formSchema = getSchema();
  // let validator = ajv(formSchema);
  // let errors = validator.iter_errors(formData);
  // let toReturn = errors.sort((val1, val2) => {
  //   const a = val1.toUpperCase();
  //   const b = val2.toUpperCase();
  //   if (a < b) return -1;
  //   else if (a > b) return 1;
  //   else return 0;
  // })
  // return toReturn;
}

export {
  getSchema,
  validate,
  validateItem
}
