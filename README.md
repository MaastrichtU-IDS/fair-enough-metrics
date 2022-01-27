# ✅ FAIR Enough metrics for research

[![Test Metrics](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml/badge.svg)](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml)

[FAIR](https://www.go-fair.org/fair-principles/) metrics tests service for Rare Disease research.

Deployed publicy at https://metrics.api.fair-enough.semanticscience.org

🗃️ Can be used with the FAIR evaluation services:

* https://fair-enough.semanticscience.org
* https://fairsharing.github.io/FAIR-Evaluator-FrontEnd

Metrics tests API built with Python and [FastAPI](https://fastapi.tiangolo.com/).


## Deploy the API

Clone the repository:

```bash
git clone https://github.com/MaastrichtU-IDS/fair-enough-metrics
cd fair-enough-metrics
```

### 🐳 Development with docker (recommended)

From the root of this repository, run the command below, and access the OpenAPI Swagger UI on http://localhost:8000

```bash
docker-compose up
```

The API will automatically reload on changes to the code.

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

## ✅ Test the Metrics API

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

