from .data_sources import DataSources
from datetime import date
import json
from ohmysportsfeedspy import MySportsFeeds


class MSFConnector:
    def __init__(self, version, api_key, password, call_file):
        self.__conn = MySportsFeeds(version=version)
        self.__conn.authenticate(api_key, password)
        self.__call_signature = {}

        self.call_signatures = {}
        with open(call_file) as f:
            self.call_signatures = json.load(f)

    @property
    def file_name(self):
        return (f'results/{self.__call_signature["feed"]}-{self.__call_signature["league"]}-'
                f'{self.__call_signature["season"]}.{self.__call_signature["format"]}')

    def get_current_season(self, league, response_format='json'):
        try:
            season_data = self.__conn.msf_get_data(league=league, force=True,
                                                   feed='current_season',
                                                   format=response_format,
                                                   fordate=date.today().strftime('%Y%m%d'))
            season_details = season_data['currentseason']['season'][0]['details']
            season = season_details['slug'].split('-')
            season[0] = int(season[0])
        except Exception as e:
            season = [1800, 'pre']

        return season

    def make_api_call(self, data_source):
        if data_source == DataSources.FILE:
            with open(self.file_name, 'r') as f:
                output = json.load(f)
        else:
            output = self.__conn.msf_get_data(league=self.__call_signature['league'], force=True,
                                              season=self.__call_signature['season'],
                                              feed=self.__call_signature['feed'],
                                              format=self.__call_signature['format'])

        return output

    def set_call_signature(self, league, season_type, call_type, season=0):
        call_signature = self.call_signatures[league][season_type][call_type]

        self.__call_signature['league'] = call_signature['league']
        self.__call_signature['feed'] = call_signature['feed']
        self.__call_signature['format'] = call_signature['format']
        self.__call_signature['season_year'] = call_signature['season_year']
        self.__call_signature['season_type'] = call_signature['season_type']
        self.__call_signature['season'] = (f'{self.__call_signature["season_year"]}-'
                                           f'{self.__call_signature["season_type"]}')

        if season > 0:
            self.update_season_in_call_signature(season)

    def update_season_in_call_signature(self, new_season):
        self.__call_signature['season_year'] = new_season
        self.__call_signature['season'] = (f'{self.__call_signature["season_year"]}-'
                                           f'{self.__call_signature["season_type"]}')
