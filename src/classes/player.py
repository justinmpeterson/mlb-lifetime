from .abstract_player import Batter, Pitcher
from .player_types import PlayerTypes


# TODO Update this to use flattened data instead. We will never invoke this class using MSF-formatted data.


class Player:
    def __init__(self, player_data):
        # print(f'--- {player_data}')
        if 'player_type' in player_data:
            if player_data['player_type'] == PlayerTypes.Pitcher.value:
                self.player = Pitcher().from_alternate_format(player_data)
            else:
                self.player = Batter().from_alternate_format(player_data)
        else:
            if player_data['player']['Position'] == PlayerTypes.Pitcher.value:
                self.player = Pitcher(player_data)
            else:
                self.player = Batter(player_data)

    def output_csv_format(self):
        return self.player.output_csv_format()

    def output_points_csv(self):
        return self.player.output_points_csv()

    def __repr__(self):
        return f'{self.player}'
