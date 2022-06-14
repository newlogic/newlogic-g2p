# Managing Programs

Programs and Cycle are at the heart of Newlogic G2P.

**TODO: Insert the diagram**

## Concepts

### Programs

Programs, sometimes also called a campaign, is defining a social program.

A program is organising when, what and how beneficiaries receive as entitlements. In itself, a program does
not do much, but use various managers to define the journey of beneficiaries in a program.

Currently few type of programs are supported:

- Cash transfer
- Mobile money
- Voucher
- Voucher for restricted cash

### Cycle

Cycle represent a distribution cycle.

### Beneficiary

A beneficiary is a registrant that is part of a program / cycle.

### Managers

There are different type of managers that define how programs and cycle are working. Each manager type has a
defined programing API that needs to be implemented in order to define how the system will work.

For all of the managers, a default implementation designed to support the most common use cases. You can
easily add your own managers if those do not fit your needs.

#### Eligibility Manager

The elegibility manager verifies if a beneficiary is eligible for a given program. The eligibility
determination can be based on data store in Newlogic G2P or on external system using API calls.

#### Entitlement Manager

The entitlement manager determine what a beneficiary is entitled to for a given cycle.

Currently entitlement manager only support monetory value. It is planed to add support for in-kind
distribution in the near future.

#### Deduplication Manager

The deduplication manager allow to define how beneficiaries are deduplicated within a program.

#### Notification Manager

The notification managers allow to notify beneficiaries of some events hapening in the programs or cycles.

#### Program Manager

#### Cycle Manager

## Type of payment instruments

### Cash Transfer

**STATUS**: Work In Progress.

Newlogic G2P can generate payment lists that can be shared with a bank to verify or execute transfers.

### Mobile m oney

### Voucher program

Newlogic G2P can generate nominative vouchers in batch ready to be printed.

The design of the vouchers can be customized by updating the voucher template.

**Warning:**

> If you plan to accept vouchers and do no plan to verify them with the server at the time of accepting then
> you should think about what security features you need to implement to avoid having them being duplicated.
>
> We recommend the use of online verification when the voucher is received or the use of secure paper.

### Voucher for restricted cash programs

Vouchers can be used in conjunction with Odoo POS to provide restricted cash solutions. Merchant can use the
Odoo POS to record what is distributed against a given voucher.
