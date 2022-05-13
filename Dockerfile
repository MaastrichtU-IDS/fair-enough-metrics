FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9


WORKDIR /app/

COPY ./requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install pytest ; fi"

COPY . /app


# Create non root user app
RUN addgroup --system app && adduser --system --group app

# Make sure all files belongs to the app user
RUN chown -R app:app /app && \
    chown -R app:app $HOME

USER app

ENV APP_MODULE=main:app


# Ensures that the python output is sent straight to terminal to see in real time
# ENV PYTHONUNBUFFERED 1

# Creates problem when installing pip packages from GitHub, and everything works without them, for the moment...
# RUN python setup.py install
# RUN pip install .

# CMD ["uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8000"]