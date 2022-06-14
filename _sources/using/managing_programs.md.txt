# Managing Programs

`Programs` and `Cycles` are at the heart of Newlogic G2P.

![Newlogic G2P Overview](https://github.com/newlogic/newlogic-g2p/raw/main/newlogic_g2p_overview.png)

## Concepts

### Programs

Programs, sometimes also called a campaign, define a social program. A program is organizing when, what and
how beneficiaries receive as entitlements. In itself, a program does not do much, but use various managers to
define the journey of beneficiaries in a program.

Currently, few types of programs are supported:

- Cash transfer
- Mobile money
- Voucher
- Voucher for restricted cash

### Cycle

Cycles represent a distribution cycle.

### Beneficiary

A beneficiary is a registrant that is part of a program/cycle.

### Managers

There are different types of managers that define how programs and cycles work. Each manager type has a
defined programming API that needs to be implemented in order to define how the system will work.

For all the managers, a default implementation is designed to support the most common use cases. You can
easily add your managers if those do not fit your needs.

#### Eligibility Manager

The eligibility manager verifies if a beneficiary is eligible for a given program. The eligibility
determination can be based on data stored in Newlogic G2P or on an external system using API calls.

#### Entitlement Manager

The entitlement manager determines what a beneficiary is entitled to for a given cycle.

Currently, entitlement managers only support monetary value. It is planned to add support for in-kind
distribution in the near future.

#### Deduplication Manager

The deduplication manager allows to define how beneficiaries are deduplicated within a program.

#### Notification Manager

The notification managers allow notifying beneficiaries of some events hapening in the programs or cycles.

#### Program Manager

#### Cycle Manager

## Type of payment instruments

### Cash Transfer

**STATUS**: Work In Progress.

Newlogic G2P can generate payment lists that can be shared with a bank to verify or execute transfers.

### Mobile money

### Voucher program

Newlogic G2P can generate nominative vouchers in batches ready to be printed.

The design of the vouchers can be customized by updating the voucher template.

::::{important}

If you plan to accept vouchers and do not plan to verify them with the server at the time of accepting then
you should think about what security features you need to implement to avoid having them being duplicated.

We recommend the use of online verification when the voucher is received or the use of secure paper.

::::

### Voucher for restricted cash programs

Vouchers can be used in conjunction with Odoo POS to provide restricted cash solutions. Merchant can use the
Odoo POS to record what is distributed against a given voucher.
