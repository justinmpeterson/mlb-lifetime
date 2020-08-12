from .draft_pick import DraftPick
from .player import Player
from .team_owner import TeamOwner
import json


class DraftPickOwner:
    def __init__(self, pick_number, owner_info):
        self.pick_number = pick_number
        self.owner_info = owner_info

    def __repr__(self):
        return ('{' +
                '"pick_number": ' + str(self.pick_number) + ', ' +
                '"owner_info": ' + str(self.owner_info) +
                '}'
                )


class Draft:
    def __init__(self, season=2000, number_of_owners=1, number_of_rounds=1, is_snake_style=True,
                 is_started=True, is_finished=False, team_owners=None, draft_picks=None):
        self.season = season
        self.number_of_owners = number_of_owners
        self.number_of_rounds = number_of_rounds
        self.is_snake_style = is_snake_style
        self.started = is_started
        self.finished = is_finished
        self.__draft_picks = [] if draft_picks is None else draft_picks
        self.__team_owners = [] if team_owners is None else team_owners

    @classmethod
    def from_json_file(cls, draft_file):
        local_draft_picks = []

        with open(draft_file, 'r') as f:
            draft_data = json.load(f)

        for pick in draft_data['draft_picks']:
            owner_obj = TeamOwner(**pick['owner'])
            player_obj = Player(pick['player']) if 'player_id' in pick['player'] else None
            local_draft_picks.append(DraftPick(pick['overall_pick_number'], pick['round_number'],
                                               pick['pick_number'], owner_obj, pick['player_is_reconciled'],
                                               pick['player_txt'], player_obj))

        return cls(team_owners=[DraftPickOwner(x['pick_number'],
                                               TeamOwner(**x['owner_info'])) for x in draft_data['owners']],
                   draft_picks=local_draft_picks,
                   **draft_data['metadata'])

    def display_draft_order(self):
        print(''.join(f'{x.pick_number}. {x.owner_info.display_name}\n' for x in self.__team_owners))

    def display_draft_picks(self, pick_slot=None):
        for o in [x for x in self.__team_owners if (pick_slot is None or
                                                    (pick_slot is not None and x.pick_number == pick_slot))]:
            print(f'{o.owner_info.display_name}')
            for pick in [x for x in self.__draft_picks if x.owner.owner_id == o.owner_info.owner_id]:
                print(f'  {pick.round_number}.{pick.pick_number} | {pick.overall_pick_number} | {pick.player_txt}')

    def finalize_draft(self):
        self.finished = True

    def get_all_reconciled_players(self):
        return [x for x in self.__draft_picks if x.player_is_reconciled]

    def get_all_unreconciled_players(self):
        return [x for x in self.__draft_picks if not x.player_is_reconciled]

    def get_owners(self):
        return [x.owner_info for x in self.__team_owners]

    def get_players_by_owner(self, owner_id):
        return [x.player for x in self.__draft_picks if x.player is not None and x.owner.owner_id == owner_id]

    def load_picks_from_file(self, pick_file):
        with open(pick_file, 'r') as dfile:
            draft_picks = list(map(lambda p: p.rstrip(), dfile.readlines()))

        overall_pick_number = 1
        current_round = 0
        for pick in draft_picks:
            current_round = current_round + 1 if overall_pick_number % self.number_of_owners == 1 else current_round
            round_pick_number = 8 if overall_pick_number % self.number_of_owners == 0 else \
                overall_pick_number % self.number_of_owners
            if current_round % 2 == 1:
                pick_owner = [x for x in self.__team_owners if x.pick_number == round_pick_number][0]
            else:
                pick_owner = [x for x in self.__team_owners if x.pick_number == (9 - round_pick_number)][0]
            self.__draft_picks.append(DraftPick(overall_pick_number, current_round, round_pick_number,
                                                pick_owner.owner_info, False, pick))
            overall_pick_number += 1

    def reconcile_players_with_data_provider(self, player_file):
        with open(player_file, 'r') as f2:
            active_players = json.load(f2)

        for pick in self.__draft_picks:
            pick_parts = pick.player_txt.split(',')
            name = pick_parts[0].strip('"')
            found_players = [x for x in active_players if f'{x["first_name"]} {x["last_name"]}' == name]
            if len(found_players) == 0:
                pass
            elif len(found_players) == 1:
                pick.set_reconciled_player(Player(found_players[0]))
            else:
                pass
                print(f'??? Found multiple players for {name} ???')

    def set_owners(self, team_owners):
        pick_num = 1
        for owner in team_owners:
            self.__team_owners.append(DraftPickOwner(pick_num, owner))
            pick_num += 1

    def __repr__(self):
        return ('{"metadata": {' +
                '"season": ' + str(self.season) + ', ' +
                '"number_of_owners": ' + str(self.number_of_owners) + ', ' +
                '"number_of_rounds": ' + str(self.number_of_rounds) + ', ' +
                '"is_snake_style": ' + ('true' if self.is_snake_style else 'false') + ', ' +
                '"is_started": ' + ('true' if self.started else 'false') + ', ' +
                '"is_finished": ' + ('true' if self.finished else 'false') + '}, ' +
                '"owners": [' + ''.join(f'{x}, ' for x in self.__team_owners).rstrip(', ') + '], ' +
                '"draft_picks": [' + ''.join(f'{x}, ' for x in self.__draft_picks).rstrip(', ') + ']' +
                '}'
                )
