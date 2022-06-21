---
description: How to install OpenG2P Deduplication Service
keywords: Deduplication Service, install, installation, openg2p, documentation
title: Installing OpenG2P Deduplication Service
toc_max: 2
---

# Installation

## Using Docker Compose

You can get started by using the docker-compose
[here](https://raw.githubusercontent.com/OpenG2P/openg2p-deduplicationservice/master/docker-compose.yml) which
starts both the server and its dependencies

```bash
docker-compose up -d
```

You will need to create the `openg2p-network` docker network if it does not exist

## Docker Image

You will need to have
[elasticsearch 7.6.1](https://www.elastic.co/downloads/past-releases/elasticsearch-7-6-1) up and running with
the following plugins installed:

- [zentity 1.6.0](https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.6.1.zip)
- analysis-phonetic
- analysis-icu

```bash
elasticsearch-plugin install https://zentity.io/releases/zentity-1.6.0-elasticsearch-7.6.1.zip
elasticsearch-plugin install analysis-phonetic
elasticsearch-plugin install analysis-icu
```

Pass `SEARCHSERVICE_ELASTIC_ENDPOINT` as an env variable to your docker pointing to your elasticsearch
instance e.g. `http://localhost:9200`

```bash
docker run -p 9200:9200 openg2p/searchservice
```

> Startup will fail if it cannot connect to Elasticsearch!
>
> {: .warning}

## Where to go next

- [Getting Started](gettingstarted.md)
