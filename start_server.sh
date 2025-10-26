#!/usr/bin/env bash

set -e  # stop if any command fails

# Go to the directory where docker-compose.yml is located
cd ~/Desktop/personal/isp-billing

# Run docker compose
docker compose up --build -d

#!/usr/bin/env bash

set -e  # stop if any command fails

# Go to the directory where docker-compose.yml is located
cd ~/Desktop/personal/isp-billing

# Run docker compose
docker compose up down

# stop running docker container
docker stop $(docker ps -a -q)


# Stop dcoker image
docker rm $(docker ps -a -q)