# Pull official python alpine image

FROM python:3.8


# Set environnement variables

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Create and set work directory

RUN mkdir /src
WORKDIR /src


# Install dependencies

RUN pip install --upgrade pip
COPY requirements.txt /src/
RUN pip install -r requirements.txt


# Copy source code

COPY . /src/
