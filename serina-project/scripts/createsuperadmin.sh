#!/bin/bash

# Set variables for coloured text

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NC='\033[0m'


# Create default superadmin account

echo "from django.contrib.auth.models import User; User.objects.create_superuser('superadmin', 'superadmin@serina.com', 'superadmin')" | docker-compose run --rm web python3 manage.py shell_plus


# Print confirmation message and exit with 1 if failed

if [ $? == 0 ]
then
    echo "Superadmin account successfully created"
    echo "${ORANGE}Please change the default superadmin username and password immediately !${NC}"
else
    echo "${RED}Error: superadmin creation failed. Try with the shell_plus utility.${NC}"
    echo -e "\tdocker-compose run --rm web python3 manage.py shell_plus"
    exit 1
fi


# Add superadmin to Administrator group

echo "from django.contrib.auth.models import User; from registration.utils.groups import promote_to_administrator; superadmin = User.objects.get(username='superadmin'); promote_to_administrator(superadmin); superadmin.save()" | docker-compose run --rm web python3 manage.py shell_plus


# Print confirmation message and exit with 2 if failed

if [ $? == 0 ]
then
    echo "Superadmin successfully added to Administrator group"
    exit 0
else
    echo "${RED}Error: superadmin could not be added to the Administrator group. Try with the shell_plus utility.${NC}"
    echo -e "\tdocker-compose run --rm web python3 manage.py shell_plus"
    exit 2
fi
