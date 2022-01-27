FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install pytest ; fi"

COPY . /app

RUN python setup.py install

ENV APP_MODULE=api.main:app

# RUN pip install -e .
## Not working in this docker image: Error loading ASGI app. Could not import module "api.main".

# CMD ["uvicorn", "api.main:app",  "--host", "0.0.0.0", "--port", "8000"]