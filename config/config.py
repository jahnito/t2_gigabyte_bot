import json


__all__ = ['Config']


class Config():
    def __init__(self, config_file: str = 'config/config.json'):
        cfg = self.read_config_file(config_file)
        self.token = cfg['bot_token']
        self.db_host = cfg['db_host']
        self.db_user = cfg['db_user']
        self.db_pass = cfg['db_pass']
        self.db_database = cfg['db_database']

    def read_config_file(self, config_file):
        with open(config_file, 'r') as conf:
            data = json.load(conf)
        return data

    def get_dsn(self) -> str:
        return f'dbname={self.db_database} user={self.db_user} '\
               f'password={self.db_pass} host={self.db_host}'

    def __str__(self):
        return self.token

    def __repr__(self):
        return self.token
