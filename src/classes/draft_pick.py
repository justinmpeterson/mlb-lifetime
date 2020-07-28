class DraftPick:
    def __init__(self, overall_pick_number, round_number, pick_number, owner, player_is_reconciled=False,
                 player_txt='', player=None):
        self.overall_pick_number = overall_pick_number
        self.round_number = round_number
        self.pick_number = pick_number
        self.owner = owner
        self.player_is_reconciled = player_is_reconciled
        self.player_txt = player_txt
        self.player = player

    def set_reconciled_player(self, reconciled_player):
        self.player = reconciled_player
        self.player_is_reconciled = True

    def __repr__(self):
        return ('{' +
                '"overall_pick_number": ' + str(self.overall_pick_number) + ', ' +
                '"round_number": ' + str(self.round_number) + ', ' +
                '"pick_number": ' + str(self.pick_number) + ', ' +
                '"owner": ' + str(self.owner) + ', ' +
                '"player_is_reconciled": ' + ('true' if self.player_is_reconciled else 'false') + ', ' +
                '"player_txt": "' + self.player_txt.replace('"', '') + '", ' +
                '"player": ' + ('{}' if self.player is None else str(self.player)) +
                '}'
                )
