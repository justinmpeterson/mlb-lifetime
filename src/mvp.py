from .classes.data_sources import DataSources
from .classes.draft import Draft
from .classes.msf_connector import MSFConnector
from .classes.season import Season
from .classes.team_owner import TeamOwner
import argparse
from dotenv import load_dotenv
import json
import os


def create_draft_file(draft_season, pick_file, draft_file, player_file):
    owner_count = int(os.getenv('MSF_FANTASY_OWNERS'))
    round_count = int(os.getenv('MSF_FANTASY_DRAFT_ROUNDS'))
    snake_style_draft = True if os.getenv('MSF_FANTASY_DRAFT_SNAKE') == 'true' else False
    owner_file = 'data/team_owners.json'
    all_owners = []
    ordered_owners = []
    draft_order_owner_ids = os.getenv('MSF_FANTASY_DRAFT_ORDER').split(',')

    with open(owner_file, 'r') as f1:
        owner_data = json.load(f1)
    for owner in owner_data:
        all_owners.append(TeamOwner(**owner))
    for pick_owner in draft_order_owner_ids:
        ordered_owners.append([x for x in all_owners if x.owner_id == int(pick_owner)][0])

    with open(player_file, 'r') as f2:
        active_players = json.load(f2)['activeplayers']['playerentry']

    draft_obj = Draft(draft_season, owner_count, round_count, snake_style_draft)
    draft_obj.set_owners(ordered_owners)
    draft_obj.load_picks_from_file(pick_file)
    draft_obj.reconcile_players_with_data_provider(active_players)
    draft_obj.finalize_draft()

    with open(draft_file, 'w') as f3:
        json.dump(json.loads(str(draft_obj)), f3)


def start_season_from_draft_data(draft_file, season_file):
    season_obj = Season().from_draft_file(draft_file)
    season_obj.start_season()
    season_obj.save_data(season_file)


def update_season_data(season_file, stat_file_name):
    season_obj = Season().from_json_file(season_file)

    with open(stat_file_name, 'r') as f:
        all_stats = json.load(f)['cumulativeplayerstats']['playerstatsentry']

    season_obj.update_player_stats(all_stats)

    season_obj.save_data(season_file)


def update_provider_data():
    call_file = 'lib/potential_api_calls.json'
    data_source = DataSources.API
    league = os.getenv('MSF_FANTASY_LEAGUE')
    file_names = {}
    msf = MSFConnector(os.getenv('MSF_VERSION'), os.getenv('MSF_API_KEY'), os.getenv('MSF_PASSWORD'), call_file)

    local_season = int(os.getenv('MSF_SEASON')) or 1776
    local_season = args.season if args.season != 1776 else local_season
    local_season_type = os.getenv('MSF_SEASON_TYPE') or 'regular'
    local_season_type = args.season_type if args.season_type != 'none' else local_season_type

    if local_season == 1776:
        current_season = msf.get_current_season(league, os.getenv('MSF_RESPONSE_FORMAT'))
        season = current_season[0]
        season_type = current_season[1]
    else:
        season = local_season
        season_type = local_season_type

    file_names['pick_data'] = f'data/drafts/{season}-{season_type}-picks.txt'
    file_names['draft_data'] = f'data/drafts/{season}-{season_type}.json'
    file_names['season_data'] = f'data/seasons/{season}-{season_type}.json'

    endpoint = 'active_players'
    msf.set_call_signature(league, season_type, endpoint, season)
    msf.make_api_call(data_source)
    file_names[endpoint] = msf.file_name

    endpoint = 'cumulative_player_stats'
    msf.set_call_signature(league, season_type, endpoint, season)
    msf.make_api_call(data_source)
    file_names[endpoint] = msf.file_name

    return season, file_names


def main():
    current_season, file_names = update_provider_data()

    if args.run_type == 'draft':
        create_draft_file(current_season, file_names['pick_data'], file_names['draft_data'],
                          file_names['active_players'])
    elif args.run_type == 'season':
        start_season_from_draft_data(file_names['draft_data'], file_names['season_data'])
    elif args.run_type == 'update':
        update_season_data(file_names['season_data'], file_names['cumulative_player_stats'])


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('--run-type', '-r', help='What type of run to do', choices=['draft', 'season', 'update'])
    parser.add_argument('--season', '-s', type=int, default=1776, help='MLB season as 4-digit year')
    parser.add_argument('--season-type', '-t', help='MLB season type', choices=['pre', 'regular', 'post'],
                        default='none')
    args = parser.parse_args()

    main()
