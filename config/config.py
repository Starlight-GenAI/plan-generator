
import configparser

class Config:
    def __init__(self, conf):
        if not isinstance(conf, dict):
            raise TypeError(f'dict expected, found {type(conf).__name__}')

        self._raw = conf
        for key, value in self._raw.items():
            setattr(self, key, value)

class ConfigWithFile:
    def __init__(self, conf):
        if not isinstance(conf, configparser.ConfigParser):
            raise TypeError(f'ConfigParser expected, found {type(conf).__name__}')

        self._raw = conf
        for key, value in self._raw.items():
            setattr(self, key, Config(dict(value.items())))

parser = configparser.ConfigParser()
config_file_name = '<path to config>'
parser.read_file(open(config_file_name))
config = ConfigWithFile(parser)