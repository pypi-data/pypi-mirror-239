import pytest

from profitpulse.account import Account, AccountCantBeDeletedError
from profitpulse.account_name import AccountName
from profitpulse.application.delete_account import (
    AccountNotFoundError,
    DeleteAccountRequester,
    ServiceDeleteAccount,
)
from profitpulse.money import Money


class DeleteAccountRequest(DeleteAccountRequester):
    @property
    def account_name(self) -> AccountName:
        return AccountName("TheAccountName")


def test_raise_error_when_account_does_not_exist():
    request = DeleteAccountRequest()
    service = ServiceDeleteAccount({})  # type: ignore
    with pytest.raises(
        AccountNotFoundError,
        match=f"Could not find an account with name '{request.account_name}'",
    ):
        service.execute(request)


def test_raise_error_when_account_cant_be_deleted():
    request = DeleteAccountRequest()
    account = Account(account_name=request.account_name, balance=Money(10))
    accounts = {request.account_name: account}

    service = ServiceDeleteAccount(accounts)  # type: ignore
    with pytest.raises(
        AccountCantBeDeletedError,
        match="Account can't be deleted",
    ):
        service.execute(request)


def test_delete_account_when_exists():
    request = DeleteAccountRequest()
    account = Account(account_name=request.account_name, balance=Money(0))
    accounts = {request.account_name: account}

    service = ServiceDeleteAccount(accounts)  # type: ignore
    service.execute(request)

    assert len(accounts) == 0  # nosec
