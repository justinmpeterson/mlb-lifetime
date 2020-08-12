from abc import ABC, abstractmethod
from math import trunc


class AbstractPlayer(ABC):
    def __init__(self, player_data):
        self.player_type = player_data['player_type']
        self.player_id = player_data['player_id']
        self.first_name = player_data['first_name']
        self.last_name = player_data['last_name']
        self.display_name = f'{self.first_name} {self.last_name}'

        self.player_position = player_data['player_position']

        # try:
        #     self.position = player_data['player_position']
        # except KeyError as ke:
        #     self.position = 'B'
        #     print(f'!!! {player_data}')

        try:
            self.team_id = player_data['team_id']
            self.team_city = player_data['team_city']
            self.team_name = player_data['team_name']
        except KeyError as ke:
            self.team_id = 0
            self.team_city = ''
            self.team_name = ''
            print(f'!!! No TEAM node found for {self.player_id}|{self.first_name}|{self.last_name}')

    @property
    @abstractmethod
    def points(self):
        pass

    @abstractmethod
    def update_stats(self, data):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Batter(AbstractPlayer):
    def __init__(self, batter_data):
        if batter_data is not None:
            super().__init__(batter_data)
            try:
                self.hits = int(batter_data['hits'])
                self.home_runs = int(batter_data['homeruns'])
                self.runs = int(batter_data['runs'])
                self.rbi = int(batter_data['runs_batted_in'])
                self.walks = int(batter_data['walks'])
                self.stolen_bases = int(batter_data['stolen_bases'])
            except KeyError as ke:
                self.hits = 0
                self.home_runs = 0
                self.runs = 0
                self.rbi = 0
                self.walks = 0
                self.stolen_bases = 0

    @property
    def points(self):
        return self.hits + self.home_runs + self.runs + self.rbi + self.walks + self.stolen_bases

    def update_stats(self, data):
        self.hits = int(data['hits'])
        self.home_runs = int(data['homeruns'])
        self.runs = int(data['runs'])
        self.rbi = int(data['runs_batted_in'])
        self.walks = int(data['walks'])
        self.stolen_bases = int(data['stolen_bases'])

    def __repr__(self):
        return ('{' +
                '"player_type": "' + self.player_type + '", ' +
                '"player_position": "' + self.player_position + '", ' +
                '"player_id": ' + str(self.player_id) + ', ' +
                '"first_name": "' + self.first_name + '", ' +
                '"last_name": "' + self.last_name + '", ' +
                '"team_id": ' + str(self.team_id) + ', ' +
                '"team_city": "' + self.team_city + '", ' +
                '"team_name": "' + self.team_name + '", ' +
                '"hits": ' + str(self.hits) + ', ' +
                '"home_runs": ' + str(self.home_runs) + ', ' +
                '"rbi": ' + str(self.rbi) + ', ' +
                '"runs": ' + str(self.runs) + ', ' +
                '"stolen_bases": ' + str(self.stolen_bases) + ', ' +
                '"walks": ' + str(self.walks) + ', ' +
                '"points": ' + str(self.points) +
                '}')


class Pitcher(AbstractPlayer):
    def __init__(self, pitcher_data=None):
        if pitcher_data is not None:
            super().__init__(pitcher_data)
            try:
                self.wins = int(pitcher_data['wins'])
                self.saves = int(pitcher_data['saves'])
                self.strikeouts = int(pitcher_data['pitching_strikeouts'])
                self.innings_pitched = trunc(float(pitcher_data['innings_pitched']))
            except KeyError as ke:
                self.wins = 0
                self.saves = 0
                self.strikeouts = 0
                self.innings_pitched = 0

    @property
    def points(self):
        return self.strikeouts + self.innings_pitched + (4 * self.wins) + (5 * self.saves)

    def update_stats(self, data):
        self.wins = int(data['wins'])
        self.saves = int(data['saves'])
        self.strikeouts = int(data['pitching_strikeouts'])
        self.innings_pitched = trunc(float(data['innings_pitched']))

    def __repr__(self):
        return ('{' +
                '"player_type": "' + self.player_type + '", ' +
                '"player_position": "' + self.player_position + '", ' +
                '"player_id": ' + str(self.player_id) + ', ' +
                '"first_name": "' + self.first_name + '", ' +
                '"last_name": "' + self.last_name + '", ' +
                '"team_id": ' + str(self.team_id) + ', ' +
                '"team_city": "' + self.team_city + '", ' +
                '"team_name": "' + self.team_name + '", ' +
                '"innings_pitched": ' + str(self.innings_pitched) + ', ' +
                '"saves": ' + str(self.saves) + ', ' +
                '"strikeouts": ' + str(self.strikeouts) + ', ' +
                '"wins": ' + str(self.wins) + ', ' +
                '"points": ' + str(self.points) +
                '}')
