from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URI: str = "https://metrics.api.fair-enough.semanticscience.org"
    HOST: str = "metrics.api.fair-enough.semanticscience.org"

    # BASE_URI: str = "https://w3id.org/fair-enough"
    # API_URL: str = f"http://localhost:8000"

    CONTACT_URL = 'https://github.com/MaastrichtU-IDS/fair-enough-metrics'
    CONTACT_NAME = 'Vincent Emonet'
    CONTACT_EMAIL = 'vincent.emonet@gmail.com'
    CONTACT_ORCID = '0000-0002-1501-1082'
    ORG_NAME = 'Institute of Data Science at Maastricht University'


settings = Settings()
