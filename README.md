# ☑️ FAIR Enough metrics for research

[![Test Metrics](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml/badge.svg)](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml)

FAIR Enough Metrics is an API for various [FAIR](https://www.go-fair.org/fair-principles) Metrics Tests, written in python, conforming to the specifications defined by the [FAIRMetrics](https://github.com/FAIRMetrics/Metrics) working group.

This API is deployed publicy at https://metrics.api.fair-enough.semanticscience.org

It can be used with the following FAIR evaluation services:

* https://fair-enough.semanticscience.org
* https://fairsharing.github.io/FAIR-Evaluator-FrontEnd

FAIR evaluation API built with [`fair-test`](https://github.com/MaastrichtU-IDS/fair-test)

## 🧑‍💻 Deploy the API

The API is built with [FastAPI](https://fastapi.tiangolo.com/), making use of python types annotations.

First, clone the repository:

```bash
git clone https://github.com/MaastrichtU-IDS/fair-enough-metrics
cd fair-enough-metrics
```

### 🐳 Development with docker (recommended)

From the root of the cloned repository, run the command below, and access the OpenAPI Swagger UI on http://localhost:8000

```bash
docker-compose up
```

> The API will automatically reload on changes to the code 🔄

### 🐍 Development without docker

Note: it has been tested only with Python 3.8

Install dependencies from the source code:

```bash
pip install -e .
```

Start the API locally on http://localhost:8000

```bash
uvicorn main:app --reload
```

### 🚀 In production with docker

We use the `docker-compose.prod.yml` file to define the production deployment configuration.

To start the stack with production config:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

> We use a reverse [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) for docker to route the services.

## ✔️ Test the Metrics Tests API

The tests are run automatically by a GitHub Action workflow at every push to the `main` branch.

Add tests in the `./tests/test_metrics.py` file. You just need to add new entries to the JSON file to test different subjects results against the metrics tests:

```python
{
    'metric_id': 'a1-access-protocol',
    'subject': 'https://w3id.org/ejp-rd/fairdatapoints/wp13/dataset/c5414323-eab1-483f-a883-77951f246972',
    'score': 1,
},
```

Run the tests in docker-compose:

```bash
docker-compose -f docker-compose.test.yml up --force-recreate
```

> You can enable more detailed logs by changing the `command:` in the `docker-compose.test.yml` file to use `pytest -s`

## ➕ Create a new FAIR Metrics Tests service

You can easily use this repository to build and publish new FAIR metrics tests. 

1. Fork this repository
2. Change the API settings in `api/config.py`
3. Use the existing tests python files in the `metrics` folder to start writing FAIR metrics tests!
4. Start your FAIR metrics tests API with `docker-compose`!

### Use persistent identifiers

We use w3id.org to define persistent identifiers for our services: https://github.com/perma-id/w3id.org

Clone your fork of the w3id.org repository:

```bash
git clone git@github.com:vemonet/w3id.org.git
```

Add the main repository to update your fork later:

```bash
git remote add fork https://github.com/perma-id/w3id.org.gi
```

Upgrade your fork to the latest version of the main repository:

```bash
git pull fork master
```

You just need to add 2 files, you can copy the `fair-enough` folder to get started quickly with our configuration:

* `README.md`: add a short description of what the persistent identifier will be used for, and who are the maintainers (providing their GitHub ID, to make sure the namespace is not changed by unauthorized people in the future). For instance:

```markdown
# My FAIR metrics tests (fair-metrics-tests)

A namespace for FAIR evaluations metrics tests

## Maintainers

- Vincent Emonet (@vemonet)
```

* `.htaccess`: define the redirections from w3id.org to your service. For instance:

```htaccess
Header set Access-Control-Allow-Origin *
Header set Access-Control-Allow-Headers DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified$
Options +FollowSymLinks
RewriteEngine on
RewriteRule ^(.*)$ https://metrics.api.fair-enough.semanticscience.org/$1 [R=302,L]
```



