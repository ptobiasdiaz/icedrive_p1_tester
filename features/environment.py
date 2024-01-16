import importlib.resources

import Ice
from behave.model import Step
from behave.runner import Context


def before_all(ctx: Context) -> None:
    """Executed at the very beginning."""
    resources_path = importlib.resources.files("icedrive")
    slice_path = resources_path.joinpath("icedrive.ice")

    if not slice_path.exists():
        raise ImportError("Cannot find icedrive.ice. Is this package installed?")

    slice_path = slice_path.absolute().as_posix()
    Ice.loadSlice(slice_path)
    ctx.communicator = Ice.initialize()
    ctx.adapter = ctx.communicator.createObjectAdapterWithEndpoints("BehaveAdapter", "tcp")
    ctx.adapter.activate()


def before_step(ctx: Context, step: Step) -> None:
    """Executed before each step execution."""
    ctx.step = step


def after_all(ctx: Context) -> None:
    """Executed after all the steps end."""
    ctx.adapter.deactivate()
    ctx.communicator.destroy()
    del ctx.communicator
