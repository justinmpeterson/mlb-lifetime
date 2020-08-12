from .abstract_player import Batter, Pitcher
from .player_types import PlayerTypes


class PlayerFactory:
    @staticmethod
    def create_player(self, player_data):
        if player_data['player_type'] == PlayerTypes.Pitcher.value:
            return Pitcher(player_data)
        else:
            return Batter(player_data)
