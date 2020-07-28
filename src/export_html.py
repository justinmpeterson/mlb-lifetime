from .website import app
import argparse


def main():
    query_string = f'season={args.season}&season_type={args.season_type}'
    output_path = f'output/wwwhtml/{args.season}/{args.season_type}'

    with app.test_client() as c:
        leaderboard = c.get(f'/leaderboard?{query_string}')
        statistics = c.get(f'/stats/all?{query_string}')

    if leaderboard.status_code == 200:
        with open(f'{output_path}/leaderboard.html', 'wb') as f1:
            f1.write(leaderboard.data)
    else:
        print(f'Not writing leaderboard.html. Status: {leaderboard.status}')

    if statistics.status_code == 200:
        with open(f'{output_path}/stats_all.html', 'wb') as f2:
            f2.write(statistics.data)
    else:
        print(f'Not writing statistics.html. Status: {statistics.status}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--season', '-s', help='MLB season as 4-digit year')
    parser.add_argument('--season-type', '-t', help='MLB season type', choices=['pre', 'regular', 'post'])
    args = parser.parse_args()

    main()
