from enum import Enum


class DataSources(Enum):
    API = 1
    FILE = 2


class DataSource:
    def __init__(self, data_source, file_name=None):
        self.file_name = file_name

        if data_source == DataSources.API:
            self.read_from_file = False
        if data_source == DataSources.FILE:
            self.read_from_file = True
