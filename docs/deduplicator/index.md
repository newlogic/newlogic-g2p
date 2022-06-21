# Overview

This building block provides an extensible entity resolution framework for finding/matching beneficiaries
usually lacking unique identities helping programs deduplicate their beneficiary lists.

Can be used as a standalone component and also integrates with OpenG2P

## Background

Government-to-persons programs must be confident of the uniqueness of beneficiaries they serve and avoid
double-dipping. A social protection transfer program, as an example, should not be paying the same individual
multiple times per period. Yet, this is a significant challenge in countries where universal unique ID
coverage, e.g., national ID, is low. The OpenG2P Deduplication Service helps alleviate this and improve
confidence in these disbursement lists by using combinations of beneficiary's attributes (e.g., name, address,
dob) to find high probabilities of duplicates. The strategy employed is called entity resolution and also
accounts for typos and representation nuisances in these attributes, e.g., names, addresses, etc

By default, it leverages [elasticsearch](https://www.elastic.co) and [zentity](https://zentity.io/) for entity
resolution but provides an easily extensible framework for adopters to add more methods, e.g. fingerprint,
facial recognition.

## Features

Currently on entity resolution is supported; however we are working on adding fingerprint identification to
the set of deduplication strategies.

<!-- ## Common use cases

@TODO

### Integrating with the ERP

@TODO

### Using as Standalone

@TODO -->

## Getting help

OpenG2P is under active development. If you need help, would like to contribute, or simply want to talk about
the project with like-minded individuals, we have a number of open channels for communication.

- To report bugs or file feature requests: use the
  [issue tracker on Github](https://github.com/openg2p/openg2p-deduplication-service/issues).

- To contribute code or documentation changes: submit a
  [pull request on Github](https://github.com/openg2p/openg2p-deduplication-service/pulls).
