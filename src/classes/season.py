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

    @property
    def unreconciled_players_by_owner(self):
        owners = []

        for owner in self.__team_owners:
            unreconciled = [x for x in self.__unreconciled_players if x.owner.owner_id == owner.owner_id]
            unreconciled.sort(key=lambda x: x.player)
            owners.append(dict(owner=owner, unreconciled_players=unreconciled))

        return owners

    @classmethod
    def from_draft_file(cls, draft_file):
        draft_data = Draft().from_json_file(draft_file)
        local_rosters = [SeasonRosterPlayer(x.owner, x.player) for x in draft_data.reconciled_players]
        local_unreconciled = [SeasonRosterPlayer(x.owner, f'"{x.player_txt}"') for x in draft_data.unreconciled_players]
        return cls(draft_data.season, False, False, draft_data.team_owners, local_rosters, local_unreconciled)

    @classmethod
    def from_json_file(cls, season_file):
        local_rosters = []

        with open(season_file, 'r') as f:
            season_data = json.load(f)

        return cls(owners=[TeamOwner(**x) for x in season_data['team_owners']],
                   rosters=[SeasonRosterPlayer(TeamOwner(**x['owner']), Player(x['player'])) for x in season_data['team_rosters']],
                   unreconciled_players=[SeasonRosterPlayer(TeamOwner(**x['owner']), f'"{x["player"]}"') for x in season_data['unreconciled_players']],
                   **season_data['metadata'])

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

    def update_player_stats(self, stat_file_name):
        with open(stat_file_name, 'r') as f:
            all_stats = json.load(f)

        for player in [x.player for x in self.__team_rosters]:
            player_stats = next((x for x in all_stats if int(x['player_id']) == player.player.player_id),
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
