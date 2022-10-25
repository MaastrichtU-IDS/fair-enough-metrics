#!/bin/bash

## Use cache:
#ssh ids3 'cd /data/deploy-services/fair-enough-metrics ; git pull ; docker-compose up prod --force-recreate --build -d'

## Without cache:
ssh ids3 'cd /data/deploy-services/fair-enough-metrics ; git pull ; docker-compose build prod --no-cache ; docker-compose down ; docker-compose up prod --force-recreate -d'
