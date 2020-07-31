#!/bin/sh -x

ID_FILE="~/.ssh/tilde.team"
OUT_DIR="output/wwwhtml/${MSF_SEASON}/${MSF_SEASON_TYPE}"
REMOTE_DIR="/home/justin/public_html/fantasy-sports/lifetime/mlb/${MSF_SEASON}/${MSF_SEASON_TYPE}"
REMOTE_SVR="justin@tilde.team"

mkdir -p ${OUT_DIR}
ssh -i ${ID_FILE} ${REMOTE_SVR} mkdir -p ${REMOTE_DIR}

python -m src.the_app --run-type=all
python -m src.export_html

scp -i ${ID_FILE} ${OUT_DIR}/stats_all.html ${REMOTE_SVR}:${REMOTE_DIR}
scp -i ${ID_FILE} ${OUT_DIR}/leaderboard.html ${REMOTE_SVR}:${REMOTE_DIR}
scp -i ${ID_FILE} ${OUT_DIR}/unreconciled_players.html ${REMOTE_SVR}:${REMOTE_DIR}