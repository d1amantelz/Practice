#!/venv/python3.10

from dataclasses import dataclass
from typing import List
from enum import Enum

''' -------------------------------------------------------------------------------------------------------------------------

Необходимо реализовать следующий функционал:
    Нужно получать данные по юзеру по его идентификатору.

    Сначала смотрим есть ли данные по юзеру в кеше, если есть, возращаем их.
    Если в кеше нет - смотрим в базе, если есть в базе, кешируем и возращаем.
    Если в базе нет, отправляем запрос по API на отдельный сервис.
    Если данные в API есть, сохраняем данные в базу, кешируем и возращаем.

ВАЖНО:
    предусмотреть гибкость решения, возможность удаления и вставки новых элементов в путь получения данных по пользователю.
    Например, может понадобиться убрать базу данных, и получать данные по пользователю сразу из API, если их нет в кеше.
    Либо, наоборот, добавить новый элемент - смотреть данные по пользователям сначала в одном API, а потом - в другом.
    Упор стоит делать именно на проработку решения в соотвествии принципам ООП, SOLID, DRY и
    использовании наиболее подходящих паттернов.

МОЖНО:
    * Писать код в методе get_user_by_id класса UserService.
    * Создавать любые другие необходимые сущности и использовать их.

ОГРАНИЧЕНИЯ:
    * Не нужно реализовывать конкретную бизнес логику классов User, CacheManager, UserRepository, ApiClient.
        Пусть у них в методах будут заглушки, но мы подразумеваем их рабочими.

НЕЛЬЗЯ:
    * Менять классы User, CacheManager, UserRepository, ApiClient и сигнатуру метода get_user_by_id класса UserService.

ДОПОЛНИТЕЛЬНО:
    * Внести любые другие обоснованные полезные изменения, описать их общим комментарием.

РЕКОМЕНДУЕТСЯ:
    * Использовать статический анализ кода и проверку код стайла.

------------------------------------------------------------------------------------------------------------------------- '''

"""
Я НАРУШИЛ ПУНКТ, О НЕИЗМЕНЕНИИ КЛАССОВ:
     Однако, без этого, не работала бы программа.
     Пришлось бы либо добавлять 'self' в сигнатуру методов,
     либо делать их статическими. Я выбрал первое.
"""


class UserNotFoundError(Exception):
    pass


class User:
    def __init__(self, user_id: int, user_name: str) -> None:
        self._id = user_id
        self._user_name = user_name


@dataclass
class Component:
    obj: object
    ctype: str


class CType(Enum):
    CACHE = 'cache'
    DB = 'db'
    API = 'api'


class CacheManager:
    def get_key(self, key: str) -> object | None:
        pass

    def set_key(self, key: str, entity: object) -> None | Exception:
        pass


class UserRepository:
    def get(self, id: int) -> User | None:
        pass

    def save(self, entity: User) -> int | Exception:
        pass


class ApiClient:
    def send_get_request(self, route: str) -> object | None | Exception:
        pass


class UserService:
    def __init__(self, components: List[Component]) -> None:
        self.components = components

    def get_user_by_id(self, user_id: int) -> User | Exception:
        pass


components = [
    Component(obj=CacheManager(), ctype=CType.CACHE),
    Component(obj=UserRepository(), ctype=CType.DB),
    Component(obj=ApiClient(), ctype=CType.API),
]


service = UserService(components)
print(service.get_user_by_id(123))
