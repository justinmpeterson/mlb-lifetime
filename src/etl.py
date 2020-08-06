import json


def main():
    players = []
    season_file = 'results/current_season-mlb--20200728.json'
    stat_file = 'results/cumulative_player_stats-mlb-2020-regular.json'
    stat_output = 'data/stats/2020-regular.json'

    with open(season_file, 'r') as f:
        curr_seas = json.load(f)

    with open(stat_file, 'r') as f:
        curr_stats = json.load(f)

    eligible_stats = curr_seas['currentseason']['season'][0]['supportedPlayerStats']

    for player in curr_stats['cumulativeplayerstats']['playerstatsentry']:
        # print(f'{player["player"]["ID"]}|{player["player"]["LastName"]}{player["player"]["FirstName"]}')
        this_player = {}
        this_player['player_id'] = player["player"]["ID"]
        this_player['first_name'] = player["player"]["FirstName"]
        this_player['last_name'] = player["player"]["LastName"]
        this_player['player_position'] = player["player"]["Position"]
        this_player['player_type'] = 'P' if player['player']['Position'] == 'P' else 'B'

        try:
            this_player['team_id'] = player['team']['ID']
            this_player['team_city'] = player['team']['City']
            this_player['team_name'] = player['team']['Name']
        except Exception as e:
            this_player['team_id'] = 0
            this_player['team_city'] = ''
            this_player['team_name'] = ''

        for stat in eligible_stats['playerStat']:
            stat_name = (stat['name'].replace('(', '')
                         .replace(')', '')
                         .replace('-', '')
                         .replace(' ', '_').lower())

            player_stat = next((x for x in player['stats'].values() if x['@abbreviation'] == stat['abbreviation']),
                               None)
            if player_stat is not None:
                this_player[stat_name] = player_stat["#text"]
                # print(f'   {player_stat["@category"]},{player_stat["@abbreviation"]},{player_stat["#text"]}')
            else:
                # print(f'***Could not find {stat["abbreviation"]}')
                this_player[stat_name] = 0

        players.append(this_player)

    with open(stat_output, 'w') as f:
        json.dump(players, f)


if __name__ == '__main__':
    main()
