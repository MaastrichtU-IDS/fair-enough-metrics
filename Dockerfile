FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install pytest ; fi"

COPY . /app

ENV APP_MODULE=main:app

# Creates problem when installing pip packages from GitHub, and everything works without them, for the moment...
# RUN python setup.py install
# RUN pip install .

# CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8000"]