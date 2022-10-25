# ☑️ FAIR Enough metrics for research

[![Test Metrics](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml/badge.svg)](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml)

An API for various core [FAIR](https://www.go-fair.org/fair-principles) Metrics Tests, written in python, conforming to the specifications defined by the [FAIRMetrics](https://github.com/FAIRMetrics/Metrics) working group.

FAIR metrics tests are API operations which test if a subject URL is complying with certain requirements defined by a community, they usually check if the resource available at the subject URL complies with the FAIR principles (Findable, Accessible, Interoperable, Reusable)

This API is deployed publicly at https://metrics.api.fair-enough.semanticscience.org

🗃️ It can be used with the following FAIR evaluation services:

* https://fair-enough.semanticscience.org
* https://fairsharing.github.io/FAIR-Evaluator-FrontEnd

This FAIR Metrics tests API has been built with the [**FAIR test**](https://maastrichtu-ids.github.io/fair-test/) python library.

## ➕ Contribute a new FAIR Metrics Tests

ℹ️ You are welcome to submit a pull request to propose to add your tests to our API in production: https://metrics.api.fair-enough.semanticscience.org

1. Fork this repository
1. Clone your forked repository
2. Copy duplicate an existing test file in the `metrics` folder,  and modify it to define your FAIR metrics tests!
3. Start your FAIR metrics tests API with `docker-compose up` to test if your FAIR metric test works as expected
3. Send us a pull request to integrate your test to our API at https://metrics.api.fair-enough.semanticscience.org
3. Once your test is published, register it in existing FAIR evaluation services.

## 🧑‍💻 Deploy the API

First, clone the repository:

```bash
git clone https://github.com/MaastrichtU-IDS/fair-enough-metrics
cd fair-enough-metrics
```

### 🐳 Development with docker (recommended)

To deploy the API in development, with automatic reload when the code changes run this command:

```bash
docker-compose up dev
```

Access the OpenAPI Swagger UI on http://localhost:8000

If you make changes to the dependencies in `pyproject.toml` you will need to rebuild the image to install the new requirements:

```bash
docker-compose up dev --build
```

Run the **tests**:

```bash
docker-compose run test
# You can pass args:
docker-compose run test pytest -s
```

Run in **production** (change the `docker-compose.yml` to your deployment solution):

Define the Bing and Google Search API keys in the `secrets.env` file that will not be committed to git:

```bash
APIKEY_BING_SEARCH=bingapikey
APIKEY_GOOGLE_SEARCH=googleapikey
```

To start the stack with production config:

```bash
docker-compose up prod -d
```

> We use a reverse [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) for docker to route the services.

### 🐍 Without docker

#### 📥️ Install dependencies

Create and activate a virtual environment if necessary:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies from the source code:

```bash
pip install -e ".[test,dev]"
```

#### Deploy the API in development

Start the API locally on http://localhost:8000

```bash
uvicorn main:app --reload
```

> The API will automatically reload on changes to the code 🔄

#### ✔️ Test the Metrics Tests API

The tests are run automatically by a GitHub Action workflow at every push to the `main` branch.

The subject URLs to test and their expected score are retrieved from the `test_test` attribute for each metric test.

Add tests in the `./tests/test_metrics.py` file. You just need to add new entries to the JSON file to test different subjects results against the metrics tests:

Run the tests locally (from the root folder):

```bash
pytest -s
```

Run the tests only for a specific metric test:

```bash
pytest -s --metric a1-metadata-protocol
```



## ➕ Create a new FAIR Metrics Tests service

You can easily use this repository to develop and publish new FAIR metrics tests.

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



