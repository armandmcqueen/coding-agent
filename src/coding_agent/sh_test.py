import os
import re

from coding_agent.sh import run


def test_run_without_timestamps_success():
    result = run('echo "Hello, World!"')
    assert result.stdout.strip() == "Hello, World!"
    assert result.stderr == ""
    assert result.returncode == 0
    assert not result.errored


def test_run_without_timestamps_error():
    result = run("command_that_does_not_exist")
    assert result.stdout == ""
    assert "command not found" in result.stderr.lower()
    assert result.returncode != 0
    assert result.errored


def test_run_with_timestamps_success():
    result = run('echo "Hello, World!"', add_timestamps=True)
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 1
    assert re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Hello, World!", lines[0])
    assert result.stderr == ""
    assert result.returncode == 0
    assert not result.errored


def test_run_with_timestamps_error():
    result = run("command_that_does_not_exist", add_timestamps=True)
    assert result.stdout == ""
    error_lines = result.stderr.strip().split("\n")
    assert len(error_lines) > 0
    assert all(
        re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", line)
        for line in error_lines
    )
    assert "command not found" in result.stderr.lower()
    assert result.returncode != 0
    assert result.errored


def test_run_multiline_output():
    result = run('echo "Line 1" && echo "Line 2"')
    assert result.stdout.strip() == "Line 1\nLine 2"
    assert result.stderr == ""
    assert result.returncode == 0
    assert not result.errored


def test_run_multiline_output_with_timestamps():
    result = run('echo "Line 1" && echo "Line 2"', add_timestamps=True)
    lines = result.stdout.strip().split("\n")
    assert len(lines) == 2
    assert all(
        re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Line \d", line)
        for line in lines
    )
    assert result.stderr == ""
    assert result.returncode == 0
    assert not result.errored


def test_run_complex_command():
    # Using 'ls' or 'dir' depending on the OS
    command = "ls" if os.name != "nt" else "dir"
    result = run(command)
    assert result.stdout != ""
    assert result.stderr == ""
    assert result.returncode == 0
    assert not result.errored


def test_run_complex_command_with_timestamps():
    command = "ls" if os.name != "nt" else "dir"
    result = run(command, add_timestamps=True)
    lines = result.stdout.strip().split("\n")
    assert len(lines) > 0
    assert all(
        re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", line) for line in lines
    )
    assert result.stderr == ""
    assert result.returncode == 0
    assert not result.errored
