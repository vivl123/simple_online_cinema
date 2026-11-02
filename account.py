from errors import CinemaError
from subscription import PLANS


class Account:
    def __init__(self, balance=0, plan_id=None):
        if type(balance) is not int or balance < 0:
            raise CinemaError("Баланс должен быть целым неотрицательным числом")
        if plan_id is not None and (
                not isinstance(plan_id, str) or plan_id not in PLANS
        ):
            raise CinemaError("Неизвестный тариф")

        self.balance = balance
        self.plan_id = plan_id

    def deposit(self, amount):
        if type(amount) is not int or amount <= 0:
            raise CinemaError("Введите положительную сумму в целых рублях")
        self.balance += amount

    def buy_plan(self, plan_id):
        if plan_id not in PLANS:
            raise CinemaError("Такого тарифа нет")
        if self.plan_id == plan_id:
            raise CinemaError("Этот тариф уже подключён")

        plan = PLANS[plan_id]
        if self.balance < plan.price:
            raise CinemaError("Недостаточно средств")

        self.balance -= plan.price
        self.plan_id = plan_id