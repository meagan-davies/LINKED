# production image

FROM python:3.10.9-slim as production

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev \
    && pip install django-extensions==3.2.3

# make sure the production requirements are included
COPY requirements/prod.txt ./requirements/prod.txt
RUN pip install -r ./requirements/prod.txt

# Install django-extensions
RUN pip install django-extensions


# files needed for production
COPY manage.py ./manage.py
COPY setup.cfg ./setup.cfg
COPY Makefile ./Makefile
COPY static ./static
COPY linkers_website ./linkers_website


# expose the port that we'll be working out of
EXPOSE 8000 

# version of Docker image for development

# base image
FROM production as development 

COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install -r ./requirements/dev.txt

# copy everything in local directory into the docker image
COPY . .
