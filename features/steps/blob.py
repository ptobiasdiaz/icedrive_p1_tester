"""Steps implementation for the blob service related tests."""

from hashlib import sha256

import Ice
import IceDrive
from behave import given, then, when
from behave.runner import Context


class DataTransfer(IceDrive.DataTransfer):
    """Implementation of a DataTransfer in order to test uploads."""
    def __init__(self, data: bytes, limit: int) -> None:
        """Init the object."""
        self.data = data
        self.index = 0
        self.limit = limit
        self.closed = False

    def read(self, size: int, current: Ice.Current) -> bytes:
        """Return a list of, at most, size bytes."""
        limit = min(size, self.limit)

        if self.index == -1:
            return b""

        retval = self.data[self.index:self.index+limit]
        self.index += limit
        if self.index > len(self.data):
            self.index = -1

        return retval

    def close(self, current: Ice.Current) -> None:
        """Close the data if needed and remove the object."""
        current.adapter.remove(current.id)
        self.closed = True


@given('The service proxy belongs to a Blob service')
def auth_service_accessible(ctx: Context) -> None:
    """Check the given proxy and perform a checkedCast in order to use it."""
    ctx.blob_service = IceDrive.BlobServicePrx.checkedCast(ctx.service_proxy)
    assert ctx.blob_service is not None


@when("I download a blob identified by {blob_id}")
def download_blob(ctx: Context, blob_id: str) -> None:
    """Download the given blob id or error."""
    try:
        data_transfer = ctx.blob_service.download(blob_id)
        assert data_transfer is not None
        assert type(data_transfer) == IceDrive.DataTransferPrx
        assert data_transfer.ice_ping() is None
        ctx.error = None
        ctx.downloaded_content = b""
        while True:
            chunk = data_transfer.read(1024)
            ctx.downloaded_content += chunk

            if not chunk:
                break

        data_transfer.close()

    except Exception as ex:
        ctx.error = ex


@when("I add a link to a blob identified by {blob_id}")
def link_blob(ctx: Context, blob_id: str) -> None:
    """Add a link to a blob id or error."""
    try:
        ctx.blob_service.link(blob_id)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I remove a link to a blob identified by {blob_id}")
def unlink_blob(ctx: Context, blob_id: str) -> None:
    """Remove a link to a blob id or error."""
    try:
        ctx.blob_service.unlink(blob_id)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@when("I upload a blob with the following content")
def upload_blob(ctx: Context) -> None:
    """Upload the content in the text."""
    ctx.data_transfer = DataTransfer(ctx.text.encode(), 2000)
    dt_prx = IceDrive.DataTransferPrx.uncheckedCast(
        ctx.adapter.addWithUUID(ctx.data_transfer),
    )

    try:
        ctx.uploaded_blob_id = ctx.blob_service.upload(dt_prx)
        ctx.error = None

    except Exception as ex:
        ctx.error = ex


@then("The generated blob id is {blob_id}")
def check_retrieved_blob_id(ctx: Context, blob_id: str) -> None:
    """Check that the last retrieved blob id matches the expectation."""
    assert ctx.uploaded_blob_id == blob_id


@then("The downloaded content is")
def check_downloaded_content(ctx: Context) -> None:
    """Check if the downloaded content match the expected."""
    expected_content = ctx.text.encode()
    assert ctx.downloaded_content == expected_content


@then("The downloaded content SHA256 is {expected_sha256}")
def check_sha256(ctx: Context, expected_sha256: str) -> None:
    """Check SHA256 sum for the downloaded content."""
    hasher = sha256(ctx.downloaded_content)
    assert hasher.hexdigest() == expected_sha256


@then("The DataTransfer object was closed")
def check_data_transfer_closed(ctx: Context) -> None:
    """Check if the DataTransfer provided to upload a file was closed gracefully."""
    assert ctx.data_transfer.closed
