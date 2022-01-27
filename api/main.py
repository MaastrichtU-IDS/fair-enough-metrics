from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from api import metrics_api
from api.config import settings

api_router = APIRouter()

# Import tests from the metrics folder:
api_router.include_router(metrics_api.router, prefix='/tests')

app = FastAPI(
    title='FAIR Metrics tests API',
    description="""FAIR Metrics tests API for resources related to research. Follows the specifications described by the [FAIRMetrics](https://github.com/FAIRMetrics/Metrics) working group.

[![Test Metrics](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml/badge.svg)](https://github.com/MaastrichtU-IDS/fair-enough-metrics/actions/workflows/test.yml)

[Source code](https://github.com/MaastrichtU-IDS/fair-enough-metrics)    
""",
    license_info = {
        "name": "MIT license",
        "url": "https://opensource.org/licenses/MIT"
    },
    contact = {
        "name": settings.CONTACT_NAME,
        "email": settings.CONTACT_EMAIL,
        "url": settings.CONTACT_URL,
        "x-id": settings.CONTACT_ORCID,
    },
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def redirect_root_to_docs():
    """Redirect the route / to /docs"""
    return RedirectResponse(url='/docs')

