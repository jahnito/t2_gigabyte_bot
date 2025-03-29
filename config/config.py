import json


__all__ = ['Config']


class Config():
    def __init__(self, config_file: str = 'config/config.json'):
        cfg = self.read_config_file(config_file)
        self.token = cfg['bot_token']

    def read_config_file(self, config_file):
        with open(config_file, 'r') as conf:
            data = json.load(conf)
        return data

    def __repr__(self):
        return self.token
