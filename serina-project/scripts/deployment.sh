#!/bin/bash

# Deployment script

# Go to projet root
cd ~/ICC-EpreuveIntegree_2019-2020


# Pull source code from repository
git pull


# Rebuild and restart the production docker containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
