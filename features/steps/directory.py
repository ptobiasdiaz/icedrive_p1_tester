"""Steps implementation to use with directory service."""

import IceDrive
from behave import given, then, when
from behave.runner import Context


@given('The service proxy belongs to a Directory service')
def auth_service_accessible(ctx: Context) -> None:
    """Check the given proxy and perform a checkedCast in order to use it."""
    ctx.directory_service = IceDrive.DirectoryServicePrx.checkedCast(ctx.service_proxy)
    assert ctx.directory_service is not None


@when("I ask for {username}'s root directory")
def get_root_dir(ctx: Context, username: str) -> None:
    """Get the root directory for username from the directory service."""
    ctx.directory = ctx.directory_service.getRoot(username)


@when("I add a link to {blob_id} named {file_name} to the retrieved directory")
def add_link(ctx: Context, blob_id: str, file_name: str) -> None:
    """Create a link to blob_id in the current directory."""
    try:
        ctx.directory.linkFile(file_name, blob_id)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I want to get the blob id of a file named {file_name}")
def get_blob_id(ctx: Context, file_name: str) -> None:
    """Get the blob id for a given file."""
    try:
        ctx.blob_id = ctx.directory.getBlobId(file_name)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I remove a link named {file_name} from the retrieved directory")
def remove_link(ctx: Context, file_name: str) -> None:
    """Remove a link in the current directory."""
    try:
        ctx.directory.unlinkFile(file_name)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I add a child directory named {child_dir} to the retrieved directory")
def add_subdir(ctx: Context, child_dir: str) -> None:
    """Add a subdirectory to the managed directory."""
    try:
        ctx.directory.createChild(child_dir)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I want to access the child directory named {child_name}")
def get_child(ctx: Context, child_name: str) -> None:
    """Get a child from current directory or fails."""
    try:
        ctx.directory = ctx.directory.getChild(child_name)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I remove a child directory named {child_name} from the retrieved directory")
def remove_directory(ctx: Context, child_name: str) -> None:
    """Remove a child directory or error."""
    try:
        ctx.directory.removeChild(child_name)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I navigate to parent directory")
def go_to_parent(ctx: Context) -> None:
    """Navitate to current directory's parent."""
    try:
        ctx.directory = ctx.directory.getParent()
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@then("The retrieved directory is valid")
def assert_directory_is_valid(ctx: Context) -> None:
    """Check that the retrieved directory is not None and is valid."""
    assert ctx.directory is not None
    ctx.directory.ice_ping()


@then("The retrieved directory has {num:d} files")
@then("The retrieved directory has {num:d} file")
def assert_number_of_files(ctx: Context, num: int) -> None:
    """Assert of the number of contained files is the expected."""
    files = ctx.directory.getFiles()
    assert len(files) == num, "The directory contains %s"


@then("The retrieved directory has {num:d} child directories")
@then("The retrieved directory has {num:d} child directory")
def assert_number_of_childs(ctx: Context, num: int) -> None:
    """Assert of the number of contained subdirectories is the expected."""
    assert len(ctx.directory.getChilds()) == num


@then("The retrieved directory has the following child directories")
def check_child_directories(ctx: Context) -> None:
    """Check the result of getChilds."""
    childs = set(ctx.directory.getChilds())
    expected_childs = set([x["directory"] for x in ctx.table])

    assert childs == expected_childs, "The directory contains %s childs" % childs


@then("The retrieved directory has the following archives")
def check_archives(ctx: Context) -> None:
    """Check the result of getChilds."""
    files = set(ctx.directory.getFiles())
    expected_files = set([x["archives"] for x in ctx.table])

    assert files == expected_files, "The directory contains %s files" % files


@then("The received blob_id is {blob_id}")
def check_blob_id(ctx: Context, blob_id: str) -> None:
    """Check the stored blob_id is the expected."""
    assert ctx.blob_id == blob_id
