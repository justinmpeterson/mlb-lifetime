from .website import app
import argparse
from dotenv import load_dotenv
import os


def do_endpoint(endpoint, filename):
    query_string = f'season={season}&season_type={season_type}'
    output_path = f'output/wwwhtml/lifetime/{league}/{season}/{season_type}'

    with app.test_client() as c:
        response = c.get(f'{endpoint}?{query_string}')

    if response.status_code == 200:
        with open(f'{output_path}/{filename}', 'wb') as f1:
            f1.write(response.data)
    else:
        print(f'Not writing {filename}. Status: {response.status}')


def main():
    do_endpoint('/leaderboard', 'leaderboard.html')
    do_endpoint('/stats/all', 'stats_all.html')
    do_endpoint('/unreconciled', 'unreconciled_players.html')


if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('--season', '-s', type=int, default=1776, help='MLB season as 4-digit year')
    parser.add_argument('--season-type', '-t', help='MLB season type', choices=['pre', 'regular', 'playoff'],
                        default='none')
    args = parser.parse_args()

    league = os.getenv('MSF_FANTASY_LEAGUE') or 'abc'
    season = int(os.getenv('MSF_SEASON')) or 1776
    season = args.season if args.season != 1776 else season
    season_type = os.getenv('MSF_SEASON_TYPE') or 'regular'
    season_type = args.season_type if args.season_type != 'none' else season_type

    main()
