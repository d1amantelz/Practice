#!/venv/python3.10

from enum import Enum
from typing import List
import abc

''' -------------------------------------------------------------------------------------------------------------
Необходимо модифицировать цену заказа в зависимости от различных условий.

Первичные условия:
    1. корпоративный юзер и доставка DHL - весь заказ дороже на 10%
    2. корпоративный юзер и доставка самовызов ИЛИ обычный юзер и доставка DHL - весь заказ дешевле на 7%
    3. корпоративный юзер - весь заказ дороже на 5%.
    4. самовывоз - весь заказ дешевле на 20%

Проверяется с первого по последний, если условие совпало - меняется заказ, последующие условия не проверяются.

Необходимо, используя паттерны, переработать существующее решение, таким образом чтобы можно было:
    - гибко изменять порядок условий
    - легко добавлять новые условия
    - гибко изменять условия проверки и изменение заказа:
        * возможны добавления проверки других параметров и изменение не только цены заказа, но и, например,
          отвественного менеджера.

Дополнительно: внести любые другие обоснованные полезные изменения, описать их общим комментарием.
------------------------------------------------------------------------------------------------------------- '''


class UserType(Enum):
    REGULAR = 'regular'
    CORPORATIVE = 'corporative'


class DeliveryType(Enum):
    DHL = 'dhl'
    PICKUP = 'pickup'


class User:
    def __init__(self, user_id: int, user_name: str,
                 user_type: UserType) -> None:
        self._id = user_id
        self._user_name = user_name
        self._user_type = user_type

    @property
    def user_type(self):
        return self._user_type


class Manager:
    def __init__(self, manager_id: int, manager_name: str) -> None:
        self._id = manager_id
        self._manager_name = manager_name


class Order:
    def __init__(self, order_id: int, user: User, delivery_type: DeliveryType,
                 price: int, manager: Manager) -> None:
        self._id = order_id
        self._price = price
        self._delivery_type = delivery_type
        self._user = user
        self._manager = manager

    @property
    def price(self):
        return self._price

    @property
    def delivery_type(self):
        return self._delivery_type

    @property
    def user(self):
        return self._user

    @property
    def manager(self):
        return self._manager

    def set_price(self, new_price: int) -> None:
        self._price = new_price

    def apply_discount_percent(self, percent: int) -> None:
        if percent < -100:
            raise ValueError(
                'Процент скидки должен быть больше или равен -100.')

        self.set_price(round(self._price * (1 + percent / 100)))


class Discount(abc.ABC):
    def __init__(self) -> None:
        self._applied = False

    @property
    def applied(self):
        return self._applied

    def set_discount_applied(self):
        self._applied = True

    @abc.abstractmethod
    def is_eligible(self, order: Order) -> bool:
        pass

    def apply(self, order: Order) -> None:
        if self.is_eligible(order):
            order.apply_discount_percent(self.DISCOUNT_PERCENT)
            self.set_discount_applied()


class CorpAndDHLDiscount(Discount):
    DISCOUNT_PERCENT = 10

    def is_eligible(self, order: Order) -> bool:
        return order.user.user_type == UserType.CORPORATIVE and order.delivery_type == DeliveryType.DHL


class CorpDHLorRegPickupDiscount(Discount):
    DISCOUNT_PERCENT = -7

    def is_eligible(self, order: Order) -> bool:
        return (order.user.user_type == UserType.CORPORATIVE and order.delivery_type == DeliveryType.PICKUP
                or order.user.user_type == UserType.REGULAR and order.delivery_type == DeliveryType.DHL)


class CorpDiscount(Discount):
    DISCOUNT_PERCENT = 5

    def is_eligible(self, order: Order) -> bool:
        return order.user.user_type == UserType.CORPORATIVE


class PickupDiscount(Discount):
    DISCOUNT_PERCENT = -20

    def is_eligible(self, order: Order) -> bool:
        return order.delivery_type == DeliveryType.PICKUP


def handle_order(handlers: List[Discount], order: Order) -> None:
    for handler in handlers:
        handler.apply(order)
        if handler.applied:
            break


user = User(user_id=1,
            user_name='First User',
            user_type=UserType.CORPORATIVE)
manager = Manager(manager_id=1,
                  manager_name='First Manager')
order = Order(order_id=1,
              price=2000,
              delivery_type=DeliveryType.PICKUP,
              user=user,
              manager=manager)

handlers = [
    CorpAndDHLDiscount(),
    CorpDHLorRegPickupDiscount(),
    CorpDiscount(),
    PickupDiscount(),
]

old_price = order.price
handle_order(handlers, order)
new_price = order.price

print(f'{old_price} -> {new_price}')
