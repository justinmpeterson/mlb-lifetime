from .draft import Draft
from .player import Player
from .team_owner import TeamOwner
import json


class SeasonRosterPlayer:
    def __init__(self, owner_info, player_info):
        self.owner = owner_info
        self.player = player_info

    def __repr__(self):
        return ('{' +
                '"owner": ' + str(self.owner) + ', ' +
                '"player": ' + str(self.player) +
                '}'
                )


class Season:
    def __init__(self, season=2000, season_started=False, season_finished=False, owners=None, rosters=None,
                 unreconciled_players=None):
        self.__top_player_count = 10
        self.season = season
        self.season_started = season_started
        self.season_finished = season_finished
        self.__team_owners = [] if owners is None else owners
        self.__team_rosters = [] if rosters is None else rosters
        self.__unreconciled_players = [] if unreconciled_players is None else unreconciled_players

    @property
    def batters(self):
        return [x for x in self.__team_rosters if x.player.player.player_type == 'B']

    
    @property
    def top_x_batters(self):
        top_x = []
        for owner in self.__team_owners:
            roster = [x for x in self.__team_rosters if x.owner.owner_id == owner.owner_id]
            batters = [x for x in roster if x.player.player.player_type == 'B']
            batters.sort(key=lambda x: x.player.player.points, reverse=True)
            top_x.extend([x for x in batters[:self.__top_player_count]])
        return top_x

    @property
    def pitchers(self):
        return [x for x in self.__team_rosters if x.player.player.player_type == 'P']
    
    @property
    def top_x_pitchers(self):
        top_x = []
        for owner in self.__team_owners:
            roster = [x for x in self.__team_rosters if x.owner.owner_id == owner.owner_id]
            pitchers = [x for x in roster if x.player.player.player_type == 'P']
            pitchers.sort(key=lambda x: x.player.player.points, reverse=True)
            top_x.extend([x for x in pitchers[:self.__top_player_count]])
        return top_x

    @property
    def owner_leaderboard(self):
        owners = []

        for owner in self.__team_owners:
            bat_points = sum(x.player.player.points for x in self.top_x_batters if x.owner.owner_id == owner.owner_id)
            pit_points = sum(x.player.player.points for x in self.top_x_pitchers if x.owner.owner_id == owner.owner_id)
            tot_points = bat_points + pit_points
            overall_points = sum(
                p.player.player.points for p in self.__team_rosters if p.owner.owner_id == owner.owner_id)

            owners.append(dict(owner_info=owner, bat_points=bat_points, pit_points=pit_points,
                               points=tot_points, overall_points=overall_points))

        owners.sort(key=lambda x: x['points'], reverse=True)
        return owners

    @property
    def rosters_by_owner(self):
        owners = []

        for owner in self.__team_owners:
            batters = [x for x in self.batters if x.owner.owner_id == owner.owner_id]
            batters.sort(key=lambda x: -x.player.player.points)
            pitchers = [x for x in self.pitchers if x.owner.owner_id == owner.owner_id]
            pitchers.sort(key=lambda x: -x.player.player.points)
            owners.append(dict(owner=owner, batters=batters, pitchers=pitchers))

        return owners

    @property
    def team_owners(self):
        return self.__team_owners

    @property
    def team_rosters(self):
        return self.__team_rosters

    @property
    def unreconciled_players(self):
        return self.__unreconciled_players

    @classmethod
    def from_draft_file(cls, draft_file):
        draft_data = Draft().from_json_file(draft_file)
        local_rosters = [SeasonRosterPlayer(x.owner, x.player) for x in draft_data.get_all_reconciled_players()]
        local_unreconciled = [SeasonRosterPlayer(x.owner, f'"{x.player_txt}"') for x in draft_data.get_all_unreconciled_players()]
        return cls(draft_data.season, False, False, draft_data.get_owners(), local_rosters, local_unreconciled)

    @classmethod
    def from_json_file(cls, season_file):
        local_rosters = []

        with open(season_file, 'r') as f:
            season_data = json.load(f)

        return cls(owners=[TeamOwner(**x) for x in season_data['team_owners']],
                   rosters=[SeasonRosterPlayer(TeamOwner(**x['owner']), Player(x['player'])) for x in season_data['team_rosters']],
                   unreconciled_players=[SeasonRosterPlayer(TeamOwner(**x['owner']), f'"{x["player"]}"') for x in season_data['unreconciled_players']],
                   **season_data['metadata'])

    def calculate_and_display_owner_leaderboard(self):
        owners = []
        print('---------- OWNER LEADERBOARD ----------')

        for owner in self.__team_owners:
            bat_points = sum(x.player.player.points for x in self.top_x_batters if x.owner.owner_id == owner.owner_id)
            pit_points = sum(x.player.player.points for x in self.top_x_pitchers if x.owner.owner_id == owner.owner_id)
            tot_points = bat_points + pit_points
            overall_points = sum(p.player.player.points for p in self.__team_rosters if p.owner.owner_id == owner.owner_id)

            owners.append(dict(owner_info=owner, bat_points=bat_points, pit_points=pit_points,
                               points=tot_points, overall_points=overall_points))

        owners.sort(key=lambda x: x['points'], reverse=True)
        print(''.join(f'"{x["owner_info"].display_name}",{x["bat_points"]},{x["pit_points"]},{x["points"]},{x["overall_points"]}\n'
                      for x in owners).rstrip('\n'))
        with open('/tmp/owners.csv', 'w', newline='', encoding='utf8') as f1:
            f1.write('"Owner","Batting","Pitching","Total","Overall"\n')
            f1.writelines([f'"{x["owner_info"].display_name}",{x["bat_points"]},{x["pit_points"]},{x["points"]},{x["overall_points"]}\n'
                           for x in owners])

    def calculate_and_display_topx_stats(self):
        csv_output = []
        player_word = 'PLAYER' if self.__top_player_count == 1 else 'PLAYERS'
        print(f'---------- SCORING STATISTICS FOR TOP {self.__top_player_count} {player_word} ----------')

        for owner in self.__team_owners:
            print(f'***** {owner.display_name}')

            local_batters = [x for x in self.top_x_batters if x.owner.owner_id == owner.owner_id]
            print(''.join(f'{x.player.output_csv_format()}\n' for x in local_batters).rstrip('\n'))
            bat_points = sum(x.player.player.points for x in local_batters)
            csv_output.extend([f'"{owner.display_name}",{x.player.output_points_csv()}\n' for x in local_batters])

            local_pitchers = [x for x in self.top_x_pitchers if x.owner.owner_id == owner.owner_id]
            print(''.join(f'{x.player.output_csv_format()}\n' for x in local_pitchers).rstrip('\n'))
            pit_points = sum(x.player.player.points for x in local_pitchers)
            csv_output.extend([f'"{owner.display_name}",{x.player.output_points_csv()}\n' for x in local_pitchers])

            # print(f'***** {owner.display_name}')
            # roster = [x.player for x in self.__team_rosters if x.owner.owner_id == owner.owner_id]
            #
            # batters = [x for x in roster if x.player.player_type == 'B']
            # batters.sort(key=lambda x: x.player.points, reverse=True)
            # print(''.join(f'{x.output_csv_format()}\n' for x in batters[:player_count]).rstrip('\n'))
            # bat_points = sum(p.player.points for p in batters[:player_count])
            # csv_output.extend([f'"{owner.display_name}",{x.output_points_csv()}\n' for x in batters[:player_count]])
            #
            # pitchers = [x for x in roster if x.player.player_type == 'P']
            # pitchers.sort(key=lambda x: x.player.points, reverse=True)
            # print(''.join(f'{x.output_csv_format()}\n' for x in pitchers[:player_count]).rstrip('\n'))
            # pit_points = sum(p.player.points for p in pitchers[:player_count])
            # csv_output.extend([f'"{owner.display_name}",{x.output_points_csv()}\n' for x in pitchers[:player_count]])

            tot_points = bat_points + pit_points
            print(f'"Batter Points",{bat_points}')
            print(f'"Pitcher Points",{pit_points}')
            print(f'"Total Points",{tot_points}')

        with open(f'/tmp/top_{self.__top_player_count}.csv', 'w', newline='', encoding='utf8') as f:
            f.write('"Owner","Type","Player","PTS"\n')
            f.writelines(csv_output)

    def display_all_standings(self):
        self.display_full_statistics()
        self.calculate_and_display_topx_stats()
        self.calculate_and_display_owner_leaderboard()
        self.display_unreconciled_players()

    def display_full_statistics(self):
        print('---------- FULL ROSTER STATISTICS ----------')
        print('"Type","Player","H","HR","RBI","R","SB","BB","PTS"')
        print('"Type","Player","IP","SV","SO","W","PTS"')

        for owner in self.__team_owners:
            print(f'***** {owner.display_name}')
            roster = [x.player for x in self.__team_rosters if x.owner.owner_id == owner.owner_id]
            roster.sort(key=lambda x: (x.player.player_type, x.player.last_name))
            for player in roster:
                print(f'{player.player.output_csv_format()}')

        with open('/tmp/batters.csv', 'w', newline='', encoding='utf8') as f1:
            f1.write('"Owner","Type","Player","H","HR","RBI","R","SB","BB","PTS"\n')
            f1.writelines([f'"{x.owner.display_name}",{x.player.output_csv_format()}\n'
                           for x in self.__team_rosters if x.player.player.player_type == 'B'])

        with open('/tmp/pitchers.csv', 'w', newline='', encoding='utf8') as f2:
            f2.write('"Owner","Type","Player","IP","SV","SO","W","PTS"\n')
            f2.writelines([f'"{x.owner.display_name}",{x.player.output_csv_format()}\n'
                           for x in self.__team_rosters if x.player.player.player_type == 'P'])

    def display_unreconciled_players(self):
        print('---------- UNRECONCILED PLAYERS ----------')

        for owner in self.__team_owners:
            print(f'{owner.display_name}')
            unreconciled = [x.player for x in self.__unreconciled_players if x.owner.owner_id == owner.owner_id]
            unreconciled.sort()
            for player in unreconciled:
                print(f'   {player}')

    def finish_season(self):
        self.season_finished = True

    def save_data(self, file_name):
        try:
            with open(file_name, 'w') as f:
                json.dump(json.loads(str(self)), f)
        except json.decoder.JSONDecodeError as jsone:
            print('UH OH')
            print(str(self))

    def start_season(self):
        self.season_started = True

    def update_player_stats(self, provider_data):
        for player in [x.player for x in self.__team_rosters]:
            player_stats = next((x for x in provider_data if x['player']['ID'] == player.player.player_id),
                                None)
            if player_stats is not None:
                player.player.update_stats(player_stats)
            else:
                print(f'!!! Could not find stats for {player.player.first_name} '
                      f'{player.player.last_name} ({player.player.player_id}) '
                      'even though he was reconciled')

    def __repr__(self):
        return ('{"metadata": {' +
                '"season": ' + str(self.season) + ', ' +
                '"season_started": ' + ('true' if self.season_started else 'false') + ', ' +
                '"season_finished": ' + ('true' if self.season_finished else 'false') + '}, ' +
                '"team_owners": [' + ''.join(f'{x}, ' for x in self.__team_owners).rstrip(', ') + '], ' +
                '"team_rosters": [' + ''.join(f'{x}, ' for x in self.__team_rosters).rstrip(', ') + '], ' +
                '"unreconciled_players": [' + ''.join(f'{x}, ' for x in self.__unreconciled_players).rstrip(', ') + ']' +
                '}'
                )
