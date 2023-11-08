import typing
from typing import Optional

from profitpulse.account import Account
from profitpulse.account_name import AccountName
from profitpulse.comment import Comment
from profitpulse.money import Money


class AccountDoesNotExistError(Exception):
    def __str__(self) -> str:
        return "Account does not exist"


class Accounts(typing.Protocol):
    def __getitem__(self, account_name: AccountName) -> Account:
        ...  # pragma: no cover

    def __setitem__(self, account_name: AccountName, account: Account):
        ...  # pragma: no cover


class DepositIntoAccountRequest(typing.Protocol):
    @property
    def account_name(self) -> AccountName:
        ...  # pragma: no cover

    @property
    def comment(self) -> Optional[Comment]:
        ...  # pragma: no cover

    @property
    def amount(self) -> Money:
        ...  # pragma: no cover


class ServiceDepositIntoAccount:
    def __init__(self, accounts: Accounts):
        self._accounts = accounts

    def execute(self, request: DepositIntoAccountRequest):
        try:
            account = self._accounts[request.account_name]
        except KeyError:
            raise AccountDoesNotExistError()

        account.deposit(request.amount, comment=request.comment)

        self._accounts[request.account_name] = account
