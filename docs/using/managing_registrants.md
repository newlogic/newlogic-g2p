# Managing Registrants

Registrants are at the heart of Newlogic G2P.

A registrant can be:

- A `group`
- An `individual`

Depending on the project's requirements, a registrant can simply contain a `name` or full biographic
information, ID document numbers, pictures, bank account number, phone number and more.

**Important**:

> When implementing a project consider only collecting the information you need.
>
> See: Data minization

## Concepts

### Individual

An `individual` is a registrant that represent a person. It will have all the fields of a `registrant` plus
some additional ones.

### Group

A group is a `registrant` that represent a set of individuals. It will have all the fields of a `registrant`
plus some additional ones.

Groups could represent:

- A houshold
- A family
- A school
- ...

Groups do not need to contain individual objects. They can just contain their number of members.

For exemple:

- Adults: 2
- Children: 3
- Elderly: 2

### Group Membership

Individuals can be part of one or more groups. They can have specific roles in a group.

By default, the following roles exists:

- Head (There can be only one per group)
- Principal recipient (There can be only one per group)
- Alternative recipient

An `admin` has the right to add other roles from the configuration menu.

An individual can be the head of a group but have no specific role in another group.

### Registrants Relations

When you need to store the relationship between registrants those relations can be uselful.

You can define relationship type between different entities:

- Group - Group
- Individual - Individual
- Individual - Group

For exemple:

- Sibling (Individual - Individual)
- Parent/Child (Individual - Individual)
- Caretaker (Individual - Group)
- Neighboor (Group - Group)

### ID Documents

Registrant can have have ID Document.

The system does not enforce uniqness of Document ID by default. If uniqness is required deduplication should
be performed.

ID Document types can be configured by an admin.

## Importing Registrants

### Import fron CSV/Excel

### Import from ODK Central

## Exporting Registrants

### Export to Excel

## API
