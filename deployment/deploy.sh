#!/usr/bin/env bash

source .env
GITHUB_USERNAME=justinmpeterson
GITHUB_REPO=mlb-lifetime
PROJECT_IMG_NAME=fantasy-lifetime-mlb
PROJECT_TAG="${MSF_SEASON}-${MSF_SEASON_TYPE}"
PKG_DOMAIN="docker.pkg.github.com"
PKG_URL="${PKG_DOMAIN}/${GITHUB_USERNAME}/${GITHUB_REPO}"
SSH_PRIVATE_KEY=$(cat ~/.ssh/tilde.team)

rm -rf src/__pycache__/
rm -rf src/classes/__pycache__/
rm -rf src/website/__pycache__/

#echo "${GITHUB_PACKAGE_TOKEN}" | docker login ${PKG_DOMAIN} -u ${GITHUB_USERNAME} --password-stdin

docker build --no-cache -f Dockerfile -t ${PROJECT_IMG_NAME}:${PROJECT_TAG} \
  --build-arg MSF_API_KEY="${MSF_API_KEY}" \
  --build-arg MSF_FANTASY_LEAGUE="${MSF_FANTASY_LEAGUE}" \
  --build-arg MSF_PASSWORD="${MSF_PASSWORD}" \
  --build-arg MSF_RESPONSE_FORMAT="${MSF_RESPONSE_FORMAT}" \
  --build-arg MSF_SEASON="${MSF_SEASON}" \
  --build-arg MSF_SEASON_TYPE="${MSF_SEASON_TYPE}" \
  --build-arg MSF_VERSION="${MSF_VERSION}" \
  --build-arg SSH_PRIVATE_KEY="${SSH_PRIVATE_KEY}" \
  .
#docker tag mlb-fantasy-lifetime:2020-regular ${PKG_URL}/${PROJECT_IMG_NAME}:${PROJECT_TAG}
#docker push ${PKG_URL}/${PROJECT_IMG_NAME}:${PROJECT_TAG}
