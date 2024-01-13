"""Steps that can be used for any service with common stuff."""

import time

import IceDrive
from behave import given, when
from behave.runner import Context


@given("The service proxy is defined in user configuration {name}")
def auth_service_available_in_userdata(ctx: Context, name: str) -> None:
    """Check the userdata configuration to find the Authentication proxy"""
    assert name in ctx.config.userdata
    ctx.service_proxy = ctx.communicator.stringToProxy(ctx.config.userdata[name])


@when("I wait for {seconds:d} seconds")
def wait_for(ctx: Context, seconds: int) -> None:
    """Wait for a given amount of seconds."""
    time.sleep(seconds)


@then("The operation returns no error")
def check_last_operation_error(ctx: Context) -> None:
    """Check if the last operation returned an error."""
    assert ctx.error is None, f"The operation raised {ctx.error}"


@then("The operation raises {exception}")
def check_child_not_exists_exception(ctx: Context, exception: str) -> None:
    """Check that the previous operation raised a given exception."""
    assert ctx.error is not None
    try:
        exc = getattr(IceDrive, exception)

    except AttributeError as ex:
        raise AttributeError(f"No exception named {exception} in IceDrive module") from ex

    assert type(ctx.error) == exc
