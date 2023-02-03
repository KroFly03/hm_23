import os

from exceptions import FileError, ParameterError, UniqueError, SortingError, ArgumentError, CommandError

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
_KEYS = {'cmd1', 'cmd2', 'value1', 'value2', 'file'}
_COMMANDS = ['filter', 'map', 'unique', 'sort', 'limit']


def create_file_path(filename):
    return os.path.join(_DATA_DIR, filename)


def get_data(filename):
    with open(create_file_path(filename)) as file:
        return file.read().split('\n')


def is_file_exist(filename):
    if not os.path.exists(create_file_path(filename)):
        raise FileError


def is_commands_correct(cmd1, cmd2):
    if not(cmd1 in _COMMANDS and cmd2 in _COMMANDS):
        raise CommandError


def execute(value, cmd, data):
    match(cmd):
        case 'filter':
            return execute_filter(value, data)
        case 'map':
            return execute_map(value, data)
        case 'unique':
            return execute_unique(value, data)
        case 'sort':
            return execute_sort(value, data)
        case 'limit':
            return execute_limit(value, data)


def is_parameters_exist(param):
    if not set(param.to_dict().keys()) >= _KEYS:
        raise ParameterError


def execute_query(data):
    is_parameters_exist(data)

    cmd1 = data.get('cmd1')
    cmd2 = data.get('cmd2')
    value1 = data.get('value1')
    value2 = data.get('value2')
    file = data.get('file')

    is_file_exist(file)
    is_commands_correct(cmd1, cmd2)

    data = get_data(file)
    data = execute(value1, cmd1, data)
    data = execute(value2, cmd2, data)

    return data


def execute_filter(value, data):
    if not value:
        raise ArgumentError

    return list(filter(lambda line: value in line, data))


def execute_map(value, data):
    if not value:
        raise ArgumentError

    return list(map(lambda line: line.split(' ')[int(value)], data))


def execute_unique(value, data):
    if value:
        raise UniqueError

    return list(set(data))


def execute_sort(value, data):
    if value not in ['asc', 'desc']:
        raise SortingError

    if not value:
        raise ArgumentError

    status = True if value == 'asc' else False
    return list(sorted(data, reverse=status))


def execute_limit(value, data):
    if not value:
        raise ArgumentError

    return data[:int(value)]
