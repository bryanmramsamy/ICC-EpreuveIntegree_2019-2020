# Pull official python image

FROM python:3.8


# Set environnement variables

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Create and set work directory

WORKDIR /usr/src/app


# Update apt and install apt dependencies

RUN apt update -y
RUN apt install netcat -y


# Upgrade pip and install pip dependencies

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy entrypoint.sh

COPY ./entrypoint.sh .


# Make entrypoint executable

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]


# Copy source code

COPY . .


# Run entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
