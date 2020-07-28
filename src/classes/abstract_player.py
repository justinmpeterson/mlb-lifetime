from abc import ABC, abstractmethod
from math import trunc


class AbstractPlayer(ABC):
    def __init__(self, player_data=None):
        self.player_type = 'R'
        self.player_id = player_data['player']['ID']
        self.first_name = player_data['player']['FirstName']
        self.last_name = player_data['player']['LastName']
        self.display_name = f'{self.first_name} {self.last_name}'
        self.position = player_data['player']['Position']
        try:
            self.team_id = player_data['team']['ID']
            self.team_city = player_data['team']['City']
            self.team_name = player_data['team']['Name']
        except KeyError as ke:
            self.team_id = 0
            self.team_city = ''
            self.team_name = ''
            print(f'!!! No TEAM node found for {self.player_id}|{self.first_name}|{self.last_name}')

    @property
    @abstractmethod
    def points(self):
        pass

    @classmethod
    @abstractmethod
    def from_alternate_format(cls, alternate_data):
        pass

    @abstractmethod
    def output_csv_format(self):
        pass

    def output_points_csv(self):
        return f'"{self.player_type}","{self.display_name}",{self.points}'

    @abstractmethod
    def update_stats(self, data):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Batter(AbstractPlayer):
    def __init__(self, batter_data=None):
        if batter_data is not None:
            super().__init__(batter_data)
            try:
                self.hits = int(batter_data['stats']['Hits']['#text'])
                self.home_runs = int(batter_data['stats']['Homeruns']['#text'])
                self.runs = int(batter_data['stats']['Runs']['#text'])
                self.rbi = int(batter_data['stats']['RunsBattedIn']['#text'])
                self.walks = int(batter_data['stats']['BatterWalks']['#text'])
                self.stolen_bases = int(batter_data['stats']['StolenBases']['#text'])
            except KeyError as ke:
                self.hits = 0
                self.home_runs = 0
                self.runs = 0
                self.rbi = 0
                self.walks = 0
                self.stolen_bases = 0

        self.player_type = 'B'

    @property
    def points(self):
        return self.hits + self.home_runs + self.runs + self.rbi + self.walks + self.stolen_bases

    @classmethod
    def from_alternate_format(cls, alternate_data):
        new_data = {}
        new_data['player'] = {}

        new_data['player']['ID'] = str(alternate_data['player_id'])
        new_data['player']['LastName'] = alternate_data['last_name']
        new_data['player']['FirstName'] = alternate_data['first_name']
        new_data['player']['Position'] = alternate_data['player_type']

        if 'team_id' in alternate_data:
            new_data['team'] = {}
            new_data['team']['ID'] = str(alternate_data['team_id'])
            new_data['team']['City'] = alternate_data['team_city']
            new_data['team']['Name'] = alternate_data['team_name']

        if 'hits' in alternate_data:
            new_data['stats'] = {}
            new_data['stats']['Hits'] = {}
            new_data['stats']['Homeruns'] = {}
            new_data['stats']['Runs'] = {}
            new_data['stats']['RunsBattedIn'] = {}
            new_data['stats']['BatterWalks'] = {}
            new_data['stats']['StolenBases'] = {}
            new_data['stats']['Hits']['#text'] = str(alternate_data['hits'])
            new_data['stats']['Homeruns']['#text'] = str(alternate_data['home_runs'])
            new_data['stats']['Runs']['#text'] = str(alternate_data['runs'])
            new_data['stats']['RunsBattedIn']['#text'] = str(alternate_data['rbi'])
            new_data['stats']['BatterWalks']['#text'] = str(alternate_data['walks'])
            new_data['stats']['StolenBases']['#text'] = str(alternate_data['stolen_bases'])

        return cls(new_data)

    def output_csv_format(self):
        return (f'"{self.player_type}","{self.display_name}",{self.hits},{self.home_runs},{self.rbi},'
                f'{self.runs},{self.stolen_bases},{self.walks},{self.points}')

    def update_stats(self, data):
        self.hits = int(data['stats']['Hits']['#text'])
        self.home_runs = int(data['stats']['Homeruns']['#text'])
        self.runs = int(data['stats']['Runs']['#text'])
        self.rbi = int(data['stats']['RunsBattedIn']['#text'])
        self.walks = int(data['stats']['BatterWalks']['#text'])
        self.stolen_bases = int(data['stats']['StolenBases']['#text'])

    def __repr__(self):
        return ('{' +
                '"player_type": "' + self.player_type + '", ' +
                '"player_id": ' + self.player_id + ', ' +
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
                self.wins = int(pitcher_data['stats']['Wins']['#text'])
                self.saves = int(pitcher_data['stats']['Saves']['#text'])
                self.strikeouts = int(pitcher_data['stats']['PitcherStrikeouts']['#text'])
                self.innings_pitched = trunc(float(pitcher_data['stats']['InningsPitched']['#text']))
            except KeyError as ke:
                self.wins = 0
                self.saves = 0
                self.strikeouts = 0
                self.innings_pitched = 0

        self.player_type = 'P'

    @property
    def points(self):
        return self.strikeouts + self.innings_pitched + (4 * self.wins) + (5 * self.saves)

    @classmethod
    def from_alternate_format(cls, alternate_data):
        new_data = {}
        new_data['player'] = {}

        new_data['player']['ID'] = str(alternate_data['player_id'])
        new_data['player']['LastName'] = alternate_data['last_name']
        new_data['player']['FirstName'] = alternate_data['first_name']
        new_data['player']['Position'] = alternate_data['player_type']

        if 'team_id' in alternate_data:
            new_data['team'] = {}
            new_data['team']['ID'] = str(alternate_data['team_id'])
            new_data['team']['City'] = alternate_data['team_city']
            new_data['team']['Name'] = alternate_data['team_name']

        if 'wins' in alternate_data:
            new_data['stats'] = {}
            new_data['stats']['Wins'] = {}
            new_data['stats']['Saves'] = {}
            new_data['stats']['PitcherStrikeouts'] = {}
            new_data['stats']['InningsPitched'] = {}
            new_data['stats']['Wins']['#text'] = str(alternate_data['wins'])
            new_data['stats']['Saves']['#text'] = str(alternate_data['saves'])
            new_data['stats']['PitcherStrikeouts']['#text'] = str(alternate_data['strikeouts'])
            new_data['stats']['InningsPitched']['#text'] = str(alternate_data['innings_pitched'])

        return cls(new_data)

    def output_csv_format(self):
        return (f'"{self.player_type}","{self.display_name}",{self.innings_pitched},{self.saves},'
                f'{self.strikeouts},{self.wins},{self.points}')

    def update_stats(self, data):
        self.wins = int(data['stats']['Wins']['#text'])
        self.saves = int(data['stats']['Saves']['#text'])
        self.strikeouts = int(data['stats']['PitcherStrikeouts']['#text'])
        self.innings_pitched = trunc(float(data['stats']['InningsPitched']['#text']))

    def __repr__(self):
        return ('{' +
                '"player_type": "' + self.player_type + '", ' +
                '"player_id": ' + self.player_id + ', ' +
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
