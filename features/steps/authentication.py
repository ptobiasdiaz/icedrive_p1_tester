import Ice
import IceDrive
from behave import given
from behave.runner import Context


@given('The service proxy belongs to an Authentication service')
def auth_service_accessible(ctx: Context) -> None:
    """Check the given proxy and perform a checkedCast in order to use it."""
    ctx.authenticator = IceDrive.AuthenticationPrx.checkedCast(ctx.service_proxy)
    assert ctx.authenticator is not None


@when("I create an user named {username} with password {password}")
def create_user(ctx: Context, username: str, password: str) -> None:
    """Create an user with given username and password."""
    try:
        ctx.created_user = ctx.authenticator.newUser(username, password)
        ctx.error = None

    except IceDrive.UserAlreadyExists as ex:
        ctx.created_user = None
        ctx.error = ex


@when("I login as user {username} using password {password}")
def login(ctx: Context, username: str, password: str) -> None:
    """Login with the given user."""
    try:
        ctx.created_user = ctx.authenticator.login(username, password)
        ctx.error = None

    except IceDrive.Unauthorized as ex:
        ctx.error = ex

@when("I remove an user named {user} with password {password}")
def remove_user(ctx: Context, user: str, password: str) -> None:
    """Remove an user using a given password."""
    try:
        ctx.authenticator.removeUser(user, password)
        ctx.error = None

    except IceDrive.Unauthorized as ex:
        ctx.error = ex


@when("I create a self stored User")
def create_local_user(ctx: Context) -> None:
    """Create a local user and store the proxy."""
    class User(IceDrive.User):
        def getUsername(self, current: Ice.Current) -> str:
            return "joseluis"

        def isAlive(self, current: Ice.Current) -> bool:
            return True


    user = User()
    ctx.created_user = IceDrive.UserPrx.uncheckedCast(ctx.adapter.addWithUUID(user))


@when("I create a non-accesible User")
def create_unaccessible_user(ctx: Context) -> None:
    """Create a UserPrx for nowhere."""
    ctx.created_user = IceDrive.UserPrx.uncheckedCast(
        ctx.communicator.stringToProxy("some_random_proxy")
    )


@when("I refresh the retrieved user")
def refresh_user(ctx: Context) -> None:
    """Rrefresh the validity of the user."""
    ctx.created_user.refresh()


@then("The user creation returned UserAlreadyExists exception")
def check_user_creation_exception(ctx: Context) -> None:
    """Check that the error was the expected one."""
    assert ctx.error is not None, "Previous call didn't raise an error"
    assert isinstance(ctx.error, IceDrive.UserAlreadyExists)


@then("The retrieved user is valid")
def user_is_valid(ctx: Context) -> None:
    """Check the stored user in order to verify its validity."""
    assert ctx.created_user is not None


@then("The retrieved user is alive")
@then("The retrieved user is not alive")
def user_is_alive(ctx: Context) -> None:
    """Check if the user is alive."""
    expected_aliveness = "not" not in ctx.step.name
    assert ctx.created_user.isAlive() is expected_aliveness


@then("The retrieved user's username is {username}")
def username_is_expected(ctx: Context, username: str) -> None:
    """Check user's username."""
    assert ctx.created_user.getUsername() == username


@then("The retrieved user can be verified")
@then("The retrieved user cannot be verified")
def user_is_verified(ctx: Context) -> None:
    """Check if the user is alive."""
    verify_result = "cannot" not in ctx.step.name
    assert ctx.authenticator.verifyUser(ctx.created_user) is verify_result


@then("The login fails with Unauthorized exception")
@then("The remove fails with Unauthorized exception")
@then("The refresh fails with Unauthorized exception")
def check_last_op_exception(ctx: Context) -> None:
    """Check that the error was the expected one."""
    assert ctx.error is not None, "Previous call didn't raise an error"
    assert isinstance(ctx.error, IceDrive.Unauthorized)
