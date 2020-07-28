class TeamOwner:
    def __init__(self, owner_id, first_name, last_name, display_name='', active=True):
        self.owner_id = owner_id
        self.first_name = first_name
        self.last_name = last_name
        self.__display_name = display_name
        self.active = active

    @property
    def display_name(self):
        return self.first_name if self.__display_name == '' else self.__display_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return ('{"owner_id": ' + str(self.owner_id) + ', ' +
                '"first_name": "' + self.first_name + '", ' +
                '"last_name": "' + self.last_name + '", ' +
                '"display_name": "' + self.display_name + '", ' +
                '"active": ' + str(self.active).lower() + '}')
