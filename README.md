# ☑️ FAIR Enough metrics for research

[![Test Metrics](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml/badge.svg)](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml)

FAIR Enough Metrics is an API for various [FAIR](https://www.go-fair.org/fair-principles) Metrics Tests, written in python, conforming to the specifications defined by the [FAIRMetrics](https://github.com/FAIRMetrics/Metrics) working group.

This API is deployed publicy at https://metrics.api.fair-enough.semanticscience.org

It can be used with the FAIR evaluation services:

* https://fair-enough.semanticscience.org
* https://fairsharing.github.io/FAIR-Evaluator-FrontEnd

> Metrics tests API built [FastAPI](https://fastapi.tiangolo.com/).


## 🧑‍💻 Deploy the API

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
uvicorn api.main:app --reload
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

