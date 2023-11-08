import abc

from profitpulse.account import Account
from profitpulse.account_name import AccountName


class AccountNotFoundError(Exception):
    def __init__(self, account_name):
        self._account_name = account_name

    def __str__(self):
        return f"Could not find an account with name '{self._account_name}'"


class DeleteAccountRequester(abc.ABC):
    @property
    def account_name(self) -> AccountName:
        ...  # pragma: no cover


class AccountsRepository(abc.ABC):
    def __getitem__(self, account_name: AccountName) -> Account:
        ...  # pragma: no cover

    def __delitem__(self, account_name: AccountName):
        ...  # pragma: no cover


class ServiceDeleteAccount:
    def __init__(self, accounts: AccountsRepository):
        self._accounts = accounts

    def execute(self, request: DeleteAccountRequester):
        try:
            account = self._accounts[request.account_name]
        except KeyError:
            raise AccountNotFoundError(account_name=request.account_name)

        account.prepare_deletion()

        del self._accounts[request.account_name]
