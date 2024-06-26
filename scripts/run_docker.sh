#!/bin/bash

# Description: This script builds and starts Docker containers as defined in the docker-compose.yml file.
# Usage: scripts/run_docker.sh
# OR
# bash scripts/run_docker.sh

# Run docker-compose
docker-compose up --build