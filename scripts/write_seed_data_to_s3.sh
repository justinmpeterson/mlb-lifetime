#!/usr/bin/env bash

source .env

BUCKET_DIR=${SEED_DATA_S3_BUCKET}/lifetime/${MSF_FANTASY_LEAGUE}/${MSF_SEASON}/${MSF_SEASON_TYPE}

aws s3 cp data/team_owners.json s3://${BUCKET_DIR}/
aws s3 cp data/drafts/${MSF_SEASON}-${MSF_SEASON_TYPE}-picks.txt s3://${BUCKET_DIR}/