"""Steps related to find and run a process."""

import os
import shutil
import subprocess
import time

from behave import given, then, when
from behave.runner import Context


def get_log_base_filename(ctx: Context) -> str:
    """Return a base file name based on the feature and scenario."""
    feature_name = ctx.feature.name.replace("/", "-")
    scenario_name = ctx.scenario.name.replace("/", "-")
    filename = f"logs/{feature_name}_{scenario_name}"
    if len(filename) > 150:
        filename = filename[:150]

    return filename


def create_dir(dirname):
    """Create a directory if it doesn't exist."""
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass


@given("The command {program} is in the PATH")
def find_program_in_path(ctx: Context, program: str) -> None:
    """Find if a program can be executed by its name."""
    assert shutil.which(program) is not None, f"The program {program} cannot be found in the PATH"


@given("I run {program} using the configuration file {configuration_file}")
def run_iceserver_with_config(ctx: Context, program: str, configuration_file: str) -> None:
    """Execute the program passing the appropriate configuration file."""
    if hasattr(ctx, "background_process"):
        if ctx.background_process.poll() is None:
            return

    base_filename = get_log_base_filename(ctx)
    create_dir("logs")
    stdout_file = open(base_filename + ".out", "w")
    stderr_file = open(base_filename + ".err", "w")

    process = subprocess.Popen(
        [f"{program}", f"--Ice.Config={configuration_file}"],
        stdout=stdout_file,
        stderr=stderr_file,
        close_fds=True,
        bufsize=0,
    )

    assert process, "Process was not created"
    ctx.add_cleanup(process.terminate)
    assert process.poll() is None, f"{program} already finished!"
    ctx.background_process = process
    time.sleep(0.1)  # time to allow the process to initialise before doing anything else


@when("I terminate the background process")
def terminate_program(ctx: Context) -> None:
    """Force the program to finish."""
    ctx.background_process.terminate()
    time.sleep(0.5)


@then("The program should terminate")
def check_program_finished(ctx: Context) -> None:
    """Check if the running process already finished."""
    poll_result = ctx.background_process.poll()
    assert poll_result is not None, f"The program didn't finish yet: {poll_result}"
