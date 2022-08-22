import configparser

Config = configparser.RawConfigParser()
Config.read('config.ini')

def convert_string_to_list(string: str, sep: str=','):
    _list = string.split(sep)
    return list(map(int, _list))


def create_config_dict() -> dict:
    dic = dict(Config.items('ExamScheduling'))

    for key, value in dic.items():
        if (value.isnumeric()):
            dic[key] = int(value)

    dic['holiday_numbers'] = convert_string_to_list(dic['holiday_numbers'])

    return dic

def get_config_dict() -> dict:
    
    if not hasattr(get_config_dict, 'config_dict'):
        get_config_dict.config_dict = create_config_dict()

    return get_config_dict.config_dict