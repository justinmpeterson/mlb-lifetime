#!/usr/bin/env bash

source .env
GITHUB_USERNAME=justinmpeterson
GITHUB_REPO=mlb-lifetime
PROJECT_IMG_NAME=fantasy-lifetime-mlb
PROJECT_TAG="${MSF_SEASON}-${MSF_SEASON_TYPE}"
PKG_DOMAIN="docker.pkg.github.com"
PKG_URL="${PKG_DOMAIN}/${GITHUB_USERNAME}/${GITHUB_REPO}"
UPLOAD_TO_GITHUB=0
BUILD_AS_ARM=0

for arg in "$@"
do
  case $arg in
    --arm)
      BUILD_AS_ARM=1
      shift
      ;;
    --github)
      UPLOAD_TO_GITHUB=1
      shift
      ;;
    *)
      shift
      ;;
  esac
done

rm -rf src/__pycache__/
rm -rf src/classes/__pycache__/
rm -rf src/website/__pycache__/

if [ ${BUILD_AS_ARM} -eq 1 ]
then
	PROJECT_TAG="${PROJECT_TAG}-arm"
fi

docker build --no-cache -f Dockerfile -t ${PROJECT_IMG_NAME}:${PROJECT_TAG} \
  --build-arg MSF_FANTASY_DRAFT_ORDER="${MSF_FANTASY_DRAFT_ORDER}" \
  --build-arg MSF_FANTASY_DRAFT_ROUNDS="${MSF_FANTASY_DRAFT_ROUNDS}" \
  --build-arg MSF_FANTASY_DRAFT_SNAKE="${MSF_FANTASY_DRAFT_SNAKE}" \
  --build-arg MSF_FANTASY_LEAGUE="${MSF_FANTASY_LEAGUE}" \
  --build-arg MSF_FANTASY_OWNERS="${MSF_FANTASY_OWNERS}" \
  --build-arg MSF_RESPONSE_FORMAT="${MSF_RESPONSE_FORMAT}" \
  --build-arg MSF_SEASON="${MSF_SEASON}" \
  --build-arg MSF_SEASON_TYPE="${MSF_SEASON_TYPE}" \
  --build-arg MSF_VERSION="${MSF_VERSION}" \
  .

if [ ${UPLOAD_TO_GITHUB} -eq 1 ]
then
	echo "${GITHUB_PACKAGE_TOKEN}" | docker login ${PKG_DOMAIN} -u ${GITHUB_USERNAME} --password-stdin
	docker tag ${PROJECT_IMG_NAME}:${PROJECT_TAG} ${PKG_URL}/${PROJECT_IMG_NAME}:${PROJECT_TAG}
	docker push ${PKG_URL}/${PROJECT_IMG_NAME}:${PROJECT_TAG}
fi
