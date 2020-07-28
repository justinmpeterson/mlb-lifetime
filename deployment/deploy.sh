#!/usr/bin/env bash

source .env
SSH_PRIVATE_KEY=$(cat ~/.ssh/tilde.team)
PROJECT_REPO_NAME=mlb-fantasy-lifetime
PROJECT_TAG="${MSF_SEASON}-${MSF_SEASON_TYPE}"

rm -rf src/__pycache__/
rm -rf src/classes/__pycache__/
rm -rf src/website/__pycache__/

docker build --no-cache -f Dockerfile -t ${PROJECT_REPO_NAME}:${PROJECT_TAG} \
  --build-arg MSF_API_KEY="${MSF_API_KEY}" \
  --build-arg MSF_FANTASY_LEAGUE="${MSF_FANTASY_LEAGUE}" \
  --build-arg MSF_PASSWORD="${MSF_PASSWORD}" \
  --build-arg MSF_RESPONSE_FORMAT="${MSF_RESPONSE_FORMAT}" \
  --build-arg MSF_SEASON="${MSF_SEASON}" \
  --build-arg MSF_SEASON_TYPE="${MSF_SEASON_TYPE}" \
  --build-arg MSF_VERSION="${MSF_VERSION}" \
  --build-arg SSH_PRIVATE_KEY="${SSH_PRIVATE_KEY}" \
  .