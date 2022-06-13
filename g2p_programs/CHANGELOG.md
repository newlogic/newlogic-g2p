Format in CHANGELOG.md

## Version[0.20] - 2022-06-13

- [FIX] Create program wizard will generate a journal for every program.
- [FIX] Beneficiaries tree view default sort order by state desc.

## Version[0.19] - 2022-06-12

- [ADD] Create new program wizard called by the custom "Create Program" button in the toolbar to require
  setting the currency, eligibility criterias, number of cycles, and entitlement.

## Version[0.18] - 2022-06-11

- [ADD] Wizard for the custom "Create Program" button
- [FIX] Approve entitlement wizard: check if fund is enough for the entitlements
- [ADD] Entitlement menu for "Finance Validator" group

## Version[0.17] - 2022-06-09

- [ADD] Custom "Create Program" button to require currency for the journal before creating the program

## Version[0.16] - 2022-06-08

- [ADD] Warning on voucher fund availability upon approval of the voucher

## Version[0.15] - 2022-06-07

- [ADD] Automatically create default managers in program creation

## Version[0.14] - 2022-06-06

- [FIX] Remove dashboard menus and tabs in UI
- [FIX] Restored Cycles tab in programs UI

## Version[0.13] - 2022-05-31

- [ADD] date_ended and date_archived in g2p.program

## Version[0.12] - 2022-05-30

- [ADD] Program status

## Version[0.11] - 2022-05-27

- [ADD] Program Fund Report
- [ADD] Cycle approver group
- [ADD] Cycle approval method
- [FIX] Assign default journal to program
- [ADD] Button in programs UI to create a new journal based on the program information
- [FIX] Refer to project journal_id for all financial transactions currency_id

## Version[0.10] - 2022-05-26

- [ADD] Add to registrant's form views the "Add to Program" wizard
- [FIX] Arrange menus and UIs of programs and cycles
- [ADD] Beneficiaries, cycles, and vouchers filters
- [ADD] Program managers filter many2many fields to limit based on program
- [FIX] Accounting integration: set journal_id in programs
- [ADD] Accounting menu
- [ADD] Report: Benificiary Accounting Journal
- [ADD] Program Fund UI

## Version[0.09] - 2022-05-25

- [FIX] Add registrants to program wizard
- [ADD] Display Beneficiaries and vouchers of a cycle/Program like SMS Marketing Mailing Contact
- [ADD] Accounting integration

## Version[0.08] - 2022-05-24

- [FIX] Minor Fixes in models and UI
- [ADD] Assign to Program Wizard

## Version[0.07] - 2022-05-20

- [ADD] partner_id (m2o res.partner) fields dynamic domain in method fields_view_get
- [ADD] UIs with program_id (m2o g2p.program) automaticall hide if loaded from a o2m table
- [FIX] UI filters for loading groups or individuals based on program target type
- [FIX] Automatically set program to all manager popup forms
- [ADD] All manager model methods

## Version[0.06] - 2022-05-19

- [ADD] ID and Phone Number eligibility managers
- [FIX] Job Queue to import eligible beneficiaries
- [ADD] Notification, Program, and Cycle Managers model and UI
- [ADD] Entitlement Manager model and UI

## Version[0.05] - 2022-05-18

- [ADD] Eligibility and Deduplication Managers
- [ADD] Eligibility and Deduplication Managers UI
- [ADD] ID and Phone number deduplication UI

## Version[0.04] - 2022-05-12

- [ADD] Created Program Membership UI
- [ADD] Created Voucher UI
- [ADD] Created Cash Voucher UI
- [ADD] Created Cycle UI
- [ADD] Created Cycle Membership UI
- [ADD] extension for Registrant UI
- [ADD] extension for Registrant attribute UI

## Version[0.03] - 2022-05-11

- [ADD] Modified and implemented initial models: voucher, cash_voucher
- [ADD] Created Programs UI

## Version[0.02] - 2022-05-10

- [ADD] Modified and implemented initial models: cycle, cycle_membership, registrant, registrant_attribute

## Version[0.01] - 2022-05-09

- [START] First release
- [ADD] Modified and implemented initial models: programs, program_membership
