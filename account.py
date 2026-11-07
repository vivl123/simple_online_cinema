
from subscription import PLANS
class Account:
    def __init__(self, balance: int = 0, plan_id: str | None = None) -> None:
        if type(balance) is not int or balance < 0:
            raise ValueError("Баланс должен быть целым неотрицательным числом")
        if plan_id is not None and (not isinstance(plan_id, str) or plan_id not in PLANS):
            raise ValueError("Неизвестный тариф")
        self.balance = balance
        self.plan_id = plan_id

    def deposit(self, amount: int) -> None:
        if type(amount) is not int or amount <= 0:
            raise ValueError("Введите положительную сумму в целых рублях")
        self.balance += amount

    def buy_plan(self, plan_id: str) -> None:
        if plan_id not in PLANS:
            raise ValueError("Такого тарифа нет")
        if self.plan_id == plan_id:
            raise ValueError("Этот тариф уже подключён")
        plan = PLANS[plan_id]
        if self.balance < plan.price:
            raise ValueError("Недостаточно средств")
        self.balance -= plan.price
        self.plan_id = plan_id
