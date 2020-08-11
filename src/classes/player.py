from .abstract_player import Batter, Pitcher
from .player_types import PlayerTypes


class Player:
    def __init__(self, player_data):
        if player_data['player_type'] == PlayerTypes.Pitcher.value:
            self.player = Pitcher(player_data)
        else:
            self.player = Batter(player_data)

    def __repr__(self):
        return f'{self.player}'
