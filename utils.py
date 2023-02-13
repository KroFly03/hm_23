import os
import re
from typing import Iterator, Union, Pattern, Any
from werkzeug.datastructures import MultiDict

from exceptions import FileError, ParameterError, UniqueError, SortingError, ArgumentError, CommandError

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, "data")
_KEYS = {'cmd1', 'cmd2', 'value1', 'value2', 'file'}
_COMMANDS = ['filter', 'map', 'unique', 'sort', 'limit', 'regex']


def create_file_path(filename: str) -> str:
    return os.path.join(_DATA_DIR, filename)


def get_data(filename: str) -> Iterator:
    with open(create_file_path(filename)) as file:
        for line in file:
            yield line


def is_file_exist(filename: str) -> bool:
    if not os.path.exists(create_file_path(filename)):
        raise FileError

    return True


def is_commands_correct(cmd1: str, cmd2: str) -> bool:
    if not(cmd1 in _COMMANDS and cmd2 in _COMMANDS):
        raise CommandError

    return True


def execute(value: Union[str, int], cmd: str, data: list):
    match cmd:
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
        case 'regex':
            return execute_regex(value, data)


def is_parameters_exist(param:  MultiDict) -> bool:
    if not set(param.to_dict().keys()) >= _KEYS:
        raise ParameterError

    return True


def execute_query(data):
    is_parameters_exist(data)

    cmd1 = data.get('cmd1')
    cmd2 = data.get('cmd2')
    value1 = data.get('value1')
    value2 = data.get('value2')
    file = data.get('file')

    is_file_exist(file)
    is_commands_correct(cmd1, cmd2)

    result = list(get_data(file))
    result = list(execute(value1, cmd1, result))
    result = list(execute(value2, cmd2, result))

    return result


def execute_filter(value: Union[str, int], data: list) -> Iterator:
    if not value:
        raise ArgumentError

    return filter(lambda line: value in line, data)


def execute_map(value: Union[str, int], data: list) -> Iterator:
    if not value:
        raise ArgumentError

    return map(lambda line: line.split(' ')[int(value)], data)


def execute_unique(value: Union[str, int], data: list) -> set:
    if value:
        raise UniqueError

    return set(data)


def execute_sort(value: Union[str, int], data: list) -> list:
    if value not in ['asc', 'desc']:
        raise SortingError

    if not value:
        raise ArgumentError

    status: bool = True if value == 'asc' else False
    return sorted(data, reverse=status)


def execute_limit(value: Union[str, int], data: list) -> list:
    if not value:
        raise ArgumentError

    return data[:int(value)]


def execute_regex(value: Any, data: list) -> Iterator:
    if not value:
        raise ArgumentError

    pattern: Pattern[str] = re.compile(value)
    return filter(lambda line: re.search(pattern, line), data)
