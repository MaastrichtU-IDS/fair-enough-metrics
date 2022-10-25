FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 AS base

ENV APP_MODULE=main:app
ENV PORT=8000
ENV PYTHONUNBUFFERED 1
# Ensures that the python output is sent straight to terminal to see it in real time:

RUN pip install --upgrade pip
WORKDIR /app
COPY . /app


# Target image used for development
FROM base AS dev

RUN pip install -e ".[test,dev]"


# Target image used in production
FROM base AS prod

RUN pip install .

# Run the API as non-root user for better security
# Create non root user 'app'
RUN addgroup --system app && adduser --system --group app
# Make sure all files belongs to the app user
RUN chown -R app:app /app && \
    chown -R app:app $HOME

USER app
