class BaseError(Exception):
    message = 'Непредвиденная ошибка'


class FileError(BaseError):
    message = 'Файл не найден'


class ParameterError(BaseError):
    message = 'Не переданы все необходимые параметры'


class ArgumentError(BaseError):
    message = 'Необходимо передать аргументы'


class UniqueError(BaseError):
    message = 'При параметре <unique> не нужно указывать аргумент'


class SortingError(BaseError):
    message = 'При параметре <sort> нужно указать <asc/desc>'


class CommandError(BaseError):
    message = 'Неправильно введены название команд'
