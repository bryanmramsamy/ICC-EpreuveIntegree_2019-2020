# Pull official python image

FROM registry.gitlab.com/bryanmramsamy/icc-epreuveintegree_2019-2020/web:latest


# Set environnement variables

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Create and set work directory

WORKDIR /usr/src/app


# Update apt and install apt dependencies

RUN apt update -y
RUN apt install gettext netcat -y


# Upgrade pip and install pip dependencies

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy source code

COPY . .


# Run entrypoint.sh

ENTRYPOINT ["/usr/src/app/scripts/entrypoint.sh"]
