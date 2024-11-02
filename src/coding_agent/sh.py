# Wrappers around subprocess
import subprocess
import threading
import time
from pathlib import Path

from pydantic import BaseModel


class ProcessOutput(BaseModel):
    stdout: str
    stderr: str
    returncode: int
    errored: bool  # if the return code is non-zero


def run(
        cmd: str,
        cwd: Path | None = None,
        add_timestamps: bool = False
) -> ProcessOutput:
    if cwd is None:
        cwd = Path(".")
    if add_timestamps:
        return run_command_with_timestamps(cmd, cwd=cwd)

    return run_without_timestamps(cmd, cwd=cwd)


def run_without_timestamps(command: str, cwd: Path) -> ProcessOutput:
    """Basic run. Returns an object including whether the code errored."""
    result = subprocess.run(
        command,
        shell=True,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=cwd,
    )
    return ProcessOutput(
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
        errored=result.returncode != 0,
    )


def _add_timestamp(stream, output_list):
    for line in iter(stream.readline, b""):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        output_list.append(f"[{timestamp}] {line.decode().strip()}")


def run_command_with_timestamps(command: str, cwd: Path) -> ProcessOutput:
    """Run a command and add timestamps to the output lines."""
    # pylint: disable=consider-using-with
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd
    )

    stdout_list: list[str] = []
    stderr_list: list[str] = []

    stdout_thread = threading.Thread(
        target=_add_timestamp, args=(process.stdout, stdout_list)
    )
    stderr_thread = threading.Thread(
        target=_add_timestamp, args=(process.stderr, stderr_list)
    )

    stdout_thread.start()
    stderr_thread.start()

    returncode = process.wait()

    stdout_thread.join()
    stderr_thread.join()

    return ProcessOutput(
        stdout="\n".join(stdout_list),
        stderr="\n".join(stderr_list),
        returncode=returncode,
        errored=returncode != 0,
    )

class Runner:
    def __init__(self, add_timestamps: bool = False):
        self.add_timestamps = add_timestamps
        self.cwd = Path(".")

    def cd(self, path: Path | str):
        self.cwd = Path(path)

    def run(self, command: str) -> ProcessOutput:
        return run(command, cwd=self.cwd, add_timestamps=self.add_timestamps)
