#!/bin/sh

OUT_DIR="output/wwwhtml/lifetime/${MSF_FANTASY_LEAGUE}/${MSF_SEASON}/${MSF_SEASON_TYPE}"
NEOCITIES_DIR="lifetime/${MSF_FANTASY_LEAGUE}/${MSF_SEASON}/${MSF_SEASON_TYPE}"

mkdir -p ${OUT_DIR}
echo -n ${NEOCITIES_API_KEY} > ~/.config/neocities/config

echo "Running the application"
python -m src.the_app --run-type=all

echo "Exporting HTML"
python -m src.export_html

echo "Uploading to Neocities"
neocities upload -d ${NEOCITIES_DIR} ${OUT_DIR}/stats_all.html
neocities upload -d ${NEOCITIES_DIR} ${OUT_DIR}/leaderboard.html
neocities upload -d ${NEOCITIES_DIR} ${OUT_DIR}/unreconciled_players.html
